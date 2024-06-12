from .patient import Patient
from .helpers import eud_calculator_dose_array, calculate_vh
import numpy as np
import sys
# List of different requests

# patient id
# age

def parameter_parser(patient : 'Patient', parameter_string: str, **kwargs):
    """
    Function that parses a patient object and a parameter string.
    Returns the equivalent parameter value for the given patient.
    """
    match parameter_string:
        case "patient id":
            return float(patient.patient_id)
        case "age":
            return float(patient.metadata["Age"])
# anti coagulant
        case "anti coagulant":
            return float(patient.metadata["AntiC"])
# gi_grade2
        case "gi_grade2":
            return float(patient.metadata["Grade2"])
# gi_grade2A
        case "gi_grade2A":
            return float(patient.metadata["Grade2A"])
# gi_grade2B
        case "gi_grade2B":
            return float(patient.metadata["Grade2B"])
# gi_grade3
        case "gi_grade3":
            return float(patient.metadata["Grade3.GI.CTCv3"])
# gi_grade2+
        case "gi_grade2+":
            return float(patient.metadata["Grade2andabove"])
# gu_grade3
        case "gu_grade3":
            return float(patient.metadata["Grade3.GU.CTCv3"])
        case str(x) if x.split(" ")[-1] == 'volume':
            organ_name = " ".join(x.split(" ")[:-1])
# CTV volume
            if organ_name == "CTV":
                actual_name = patient.actual_structure_names[organ_name]
                dx,dy = list(patient.rtdose_dose.PixelSpacing) 
                dz = float(patient.rtdose_dose.GridFrameOffsetVector[1] - patient.rtdose_dose.GridFrameOffsetVector[0])
                # organ_volume = np.prod(np.shape(patient.structure_indices[actual_name])) * dx*dy*dz / 1000
                return np.prod(np.shape(patient.structure_indices[actual_name])) * dx*dy*dz / 1000
# prostate volume
# bladder volume
# bladder wall volume
# rectum volume
# rectal wall volume
            metadata_dict = {"prostate"     :"Pros.Vol.CC",
                             "bladder"      :"Blad.Vol.CC",
                             "bladder wall" :"Blad.W.Vol.CC",
                             "rectum"       :"Rec.Vol.CC",
                             "rectal wall"  :"Rec.W.Vol.CC",
                             }
            return float(patient.metadata[metadata_dict[organ_name]])
# EUD(n=0.42) rectal wall   
        case str(x) if x[:5]=="EUD(n":
            organ_name = x.split(")")[-1][1:]
            actual_name = patient.actual_structure_names[organ_name]
            if all(x in list(kwargs.keys()) for x in ["n", "dose_array"]): # If the values are passed as kwargs
                n = kwargs["n"]
                dose_array = kwargs["dose_array"]
            else:
                n = float(x.split("(")[-1].split(")")[0].split("=")[-1])
                dose_array = patient.rtdose_dose.pixel_array * patient.rtdose_dose.DoseGridScaling
            dose_array = dose_array[patient.structure_indices[actual_name]]
            return eud_calculator_dose_array(dose_array, n)
# D_4.0% bladder wall
        case str(x) if x[:2]=="D_" and x[5] == "%":
            p = float(x[2:5])
            organ_name =  " ".join(x.split(" ")[1:])
            actual_name = patient.actual_structure_names[organ_name]
            if "c" in list(kwargs.keys()):
                return patient.calculate_dvh_parameter(actual_name, "D_{:3.1f}_%".format(p), pydicom_rtdose=patient.unkelbach_rbe_weighed_dose)    
            return patient.calculate_dvh_parameter(actual_name, "D_{:3.1f}_%".format(p))
# Dose_V_10.0_Gy rectum
        case str(x) if x[:6]=="Dose_V" and x[12:14] == "Gy":
            d = float(x.split("_")[2])
            organ_name =  " ".join(x[9:].split(" ")[1:])
            actual_name = patient.actual_structure_names[organ_name]

            if "dose_array" in list(kwargs.keys()): # If the values are passed as kwargs
                dose_array = kwargs["dose_array"]
            else:
                dose_array = patient.rtdose_dose.pixel_array * patient.rtdose_dose.DoseGridScaling

            dose_array = dose_array[patient.structure_indices[actual_name]]
            return calculate_vh(dose_array, stepsize=d)[1][1] * 100
            # return patient.calculate_dvh_parameter(actual_name, "V_{:4.1f}_Gy".format(d))
# LET_V_0.2_kev_um bladder
        case str(x) if x[:6]=="LET_V_" and x[10:16] == "kev_um":
            l = float(x.split("_")[2])
            organ_name =  " ".join(x.split(" ")[1:])
            actual_name = patient.actual_structure_names[organ_name]
            let_arr = patient.rtdose_letd.pixel_array * patient.rtdose_letd.DoseGridScaling
            let_arr = let_arr[patient.structure_indices[actual_name]]
            return calculate_vh(let_arr,stepsize=l)[1][1]*100
# DoseAndLET_V_ 5.0_Gy_0.2_kev_um bladder
        case str(x) if x[:13] == "DoseAndLET_V_":
            d = float(x.split("_")[2])
            delta_dose = d 
            if d == 0:
                delta_dose = 0.1
            l = float(x.split("_")[4])
            organ_name =  " ".join(x[15:].split(" ")[1:])
            actual_name = patient.actual_structure_names[organ_name]
            try:
                rv = patient.dvh_above_let_value(l, actual_name, delta_dose=delta_dose)[1][1]
            except IndexError:
                rv = 0
            return rv
# DoseTimesLET_V_ 17.0_Gy_kev_um bladder wall
        case str(x) if x[:15] == "DoseTimesLET_V_":
            dl = float(x.split("_")[2])
            organ_name =  " ".join(x[19:].split(" ")[1:])
            actual_name = patient.actual_structure_names[organ_name]
            dose = patient.rtdose_dose.pixel_array * patient.rtdose_dose.DoseGridScaling
            let  = patient.rtdose_letd.pixel_array * patient.rtdose_letd.DoseGridScaling
            return 100*calculate_vh((dose*let)[patient.structure_indices[actual_name]], stepsize=dl)[1][1]
        
        # unkelbach cases
        # unkel c={:4.2f} --- example will be like 
        # 0 1 2 3 4 5 6 7 8 9 10 11
        # u n k e l   c = 0 . 0  9
        # unkel c=0.09 EUD(n=9.99) rectum
        case str(x) if x[:8] == "unkel c=":
            c = float(x.split("=")[1].split(" ")[0])
            n = 0.04
            patient.set_unkelbach_rbe_weighed_dose(c=c)
            unkelbach_dose_array = patient.unkelbach_rbe_weighed_dose.pixel_array * patient.unkelbach_rbe_weighed_dose.DoseGridScaling
            param_string_without_unkel = " ".join(x.split(" ")[2:])
            return parameter_parser(patient, param_string_without_unkel, c=c, n=n, dose_array=unkelbach_dose_array)
        # RBE1.1 EUD(n=0.42) rectal wall   
        case str(x) if x[:6] == "RBE1.1":
            param_string_without_RBE11 = x.replace("RBE1.1 ","")
            return parameter_parser(patient, param_string_without_RBE11)

    

            

if "test" in sys.argv:
    p = Patient("/mnt/d/simulation_data_dicom/499","default")
    param="patient id";print("{} = {}".format(param,parameter_parser(p,param)))
    param="age";print("{} = {}".format(param,parameter_parser(p,param)))
    param="anti coagulant";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gi_grade2";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gi_grade2A";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gi_grade2B";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gi_grade3";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gu_grade3";print("{} = {}".format(param,parameter_parser(p,param)))
    param="gi_grade2+";print("{} = {}".format(param,parameter_parser(p,param)))
    param="prostate volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="CTV volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="bladder volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="bladder wall volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="rectum volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="rectal wall volume";print("{} = {}".format(param,parameter_parser(p,param)))
    param="EUD(n=0.33) bladder";print("{} = {}".format(param,parameter_parser(p,param)))
    param="D_4.0% rectum";print("{} = {}".format(param,parameter_parser(p,param)))
    param="Dose_V_ 2.0_Gy rectum";print("{} = {}".format(param,parameter_parser(p,param)))
    param="LET_V_3.2_kev_um bladder";print("{} = {}".format(param,parameter_parser(p,param)))
    param="DoseAndLET_V_16.0_Gy_2.8_kev_um bladder";print("{} = {}".format(param,parameter_parser(p,param)))
    param="DoseTimesLET_V_ 123.0_Gy_kev_um rectal wall";print("{} = {}".format(param,parameter_parser(p,param)))
            
        



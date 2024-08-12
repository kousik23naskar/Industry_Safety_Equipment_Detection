import os,sys
import yaml
from SafetyEquipmentDetection.logger import logging
from SafetyEquipmentDetection.exception import AppException
from SafetyEquipmentDetection.entity.config_entity import ModelTrainerConfig
from SafetyEquipmentDetection.entity.artifacts_entity import ModelTrainerArtifact



class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config


    

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            os.system("unzip data.zip")
            os.system("rm data.zip")
            # Construct the absolute path to the data.yaml file
            data_yaml_path = os.path.join(os.getcwd(), 'data.yaml')

            # Load the existing data.yaml file
            with open(data_yaml_path, 'r') as file:
                data_yaml = yaml.safe_load(file)

            # Update paths in the data.yaml dictionary
            data_yaml['train'] = os.path.join(os.getcwd(), 'train/images')
            data_yaml['val'] = os.path.join(os.getcwd(), 'valid/images')
            data_yaml['test'] = os.path.join(os.getcwd(), 'test/images')

            yaml_content = {
                'train': data_yaml['train'],
                'val': data_yaml['val'],
                'test': data_yaml['test'],
                'nc': data_yaml['nc'],
                'names': data_yaml['names']
            }

            # Write the updated data back to the data.yaml file
            with open(data_yaml_path, 'w') as file:
                yaml.dump(yaml_content, file, default_flow_style=None)

            print(f"data.yaml file has been updated at: {data_yaml_path}")

            '''with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print("YOLO model name: ",model_config_file_name)'''

            os.system(f"yolo task=detect mode=train model={self.model_trainer_config.weight_name} data=./data.yaml epochs={self.model_trainer_config.no_epochs} imgsz=640 save=True")


            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            os.system(f"cp runs/detect/train/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")
            os.system(f"cp runs/detect/train/weights/best.pt {os.getcwd()}")
           
            #os.system("rm -rf yolov8m.pt")
            os.system(f"rm -rf {self.model_trainer_config.weight_name}")
            os.system("rm -rf train")
            os.system("rm -rf valid")
            os.system("rm -rf test")
            os.system("rm -rf data.yaml")
            os.system("rm -rf runs")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="artifacts/model_trainer/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as e:
            raise AppException(e, sys)

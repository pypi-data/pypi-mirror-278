import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from . import *


class Torch_Manager():
    def __init__(self):
        self._connectedToServer = False
        self._sessionCreated = False
        self.allConfigsDone = False
        self.modelJson = None
        self.optimizerConfig = None
        self.loss = None
        self.metricsList = None
        self.lossWeights = None
        self.weightedMetrics = None
        self.callbackList = None
    

    def initiateSessionRequest(self):
        print("\n--------------------------------------------------------------------------------------------------")

        if self.allConfigsDone == False:
            print()
            print("PLEASE CONFIGURE THE MODEL FIRST !!\n")
            print("--------------------------------------------------------------------------------------------------\n")
            return

        credentialServer_ipAddress = input("Enter the IP Address of the Server : ")

        connectedToServer = False

        email, password = None, None

        try:
            requestURL = f"http://{credentialServer_ipAddress}:6666/serverRunning"
            response = requests.get(requestURL)
            if response.status_code == 200:
                data = response.json()
                if data['message'] == "Running":
                    print()
                    print("YOU HAVE CONNECTED TO THE SERVER !!")
                    print()
                    connectedToServer = True

                    # email = input("Enter Your Account Email Address : ")
                    # password = input("Enter Your Account Password : ")
                    # jsMsg = json.dumps({"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password})
                    # requestURL = f"http://{credentialServer_ipAddress}:5555/check_node?message={jsMsg}"

                    # try:
                    #     response = requests.get(requestURL)

                    #     if response.status_code == 200:
                    #         if(response.json()['message'] == "VERIFIED"):
                    #             print()
                    #             print("CREDENTIALS VERIFIED !!")
                    #             print()
                    #             credentialsVerified = True
                    #         else:
                    #             print()
                    #             print("INVALID EMAIL OR PASSWORD !!")
                    #             print("--------------------------------------------------------------------------------------------------\n")
                    #             credentialsVerified = False
                    #             return
                    #     else:
                    #         pass
                    # except Exception as error:
                    #     print()
                    #     print(f"THE FOLLOWING ERROR OCCURED WHEN VERIFING THE CREDENTIALS : {error}")
                    #     print("--------------------------------------------------------------------------------------------------\n")
                    #     credentialsVerified = False
                    #     return

                else:
                    print("SERVER IS NOT RUNNING RIGHT NOW !!!")
                    print("--------------------------------------------------------------------------------------------------\n")
                    connectedToServer = False
                    return
        except requests.exceptions.ConnectionError:
            print()
            print("EITHER SERVER IS NOT RUNNING RIGHT NOW OR THE IP ADDRESS ENTERED IS INCORRECT\nPLEASE CHECK THE ENTERED IP ADDRESS OR ELSE TRY AGAIN LATER")
            print("--------------------------------------------------------------------------------------------------\n")
            connectedToServer = False
            return
        except Exception as error:
            print()
            print(f"THE FOLLOWING ERROR OCCURED WHEN CONNECTING TO THE SERVER : {error}")
            print("--------------------------------------------------------------------------------------------------\n")
            credentialsVerified = False
            return

        if(not connectedToServer):
            print()
            print("YOUR ARE NOT CONNECTED TO THE SERVER !!")
            print("PLEASE CONNECT TO THE SERVER FIRST !!")
            print("--------------------------------------------------------------------------------------------------\n")
            return

        try:
            email = input("Enter Your Account Email Address : ")
            password = input("Enter Your Account Password : ")
            jsMsg = json.dumps({"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password})
            requestURL = f"http://{credentialServer_ipAddress}:6666/requestSessionCreation?message={jsMsg}"
            response = requests.get(requestURL)
            if response.status_code == 200:
                data = response.json()
                if data['message'] == "Request Submitted":
                    print()
                    print("THE REQUEST WAS SUBMITTED SUCCESSFULLY !!")
                    print("INITIALIZE YOU SESSION USING YOUR DESKTOP APPLICATION !!")
                    print()
                    self._sessionCreated = True
                    self._connectedToServer = True
                    print("--------------------------------------------------------------------------------------------------\n")
                    return
                else:
                    print()
                    print(data['message'])
                    print("--------------------------------------------------------------------------------------------------\n")
                    return
            else:
                print()
                print("SESSION COULD NOT BE CREATED !!")
                print(response.json()['message'])
                print("--------------------------------------------------------------------------------------------------\n")
                return
        except Exception as error:
            print()
            print(f"THE FOLLOWING ERROR OCCURED WHEN CREATING THE SESSION : {error}")
            print("--------------------------------------------------------------------------------------------------\n")
            return

    def validModelLayers(self, layers):
        for layer in layers:
            if not isinstance(layer, nn.Module):
                return False
        return True

    def InformationTransfer(self, model):
        self.setModel(model)
        pass

    def setModel(self, model):
        if isinstance(model, nn.Module):
            self.modelJson = str(model)
            if self.validModelLayers(model.modules()) == False:
                print("Invalid Model Layers Given !!!")
                self.allConfigsDone = False
                self.modelJson = None
                return
            else:
                print("Model Configurations has been Succesfully Noted Down !!")

            if not model.optimizer:
                print("Model has no optimizer")
                print("Please Compile the Model before Sending the Model")
                return
            self.setOptimizer(model.optimizer)
            self.setLoss(model.loss)
            self.setMetrics(model.metrics)
            self.allConfigsDone = True
        else:
            print("Pass a valid model")

    def setOptimizer(self, optimizer):
        if optimizer:
            self.optimizerConfig = optimizer.state_dict()

    def setLoss(self, loss):
        self.loss = loss

    def setMetrics(self, metrics):
        self.metricsList = metrics

    def printAllConfigs(self):
        print("Model Json : ", self.modelJson)
        print("Optimizer Config : ", self.optimizerConfig)
        print("Loss : ", self.loss)
        print("Metrics : ", self.metricsList)

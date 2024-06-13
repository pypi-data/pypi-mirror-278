from . import *

class Tensorflow_Manager():
    def __init__(self) -> None:
        self._connectedToServer = False
        self._sessionCreated = False
        self.allConfigsDone = False
        self.modelJson = None       # model.to_json()  
        self.optimizerConfig = None # model.optimizer.get_config()
        self.metricsList = None     # model.compiled_metrics._user_metrics
        self.loss = None            # model.compiled_loss._user_losses
        self.lossWeights = None     # model.compiled_loss._user_loss_weights
        self.weightedMetrics = None # model.compiled_metrics._user_weighted_metrics
        
        self.epoch = None
        self.callbackList = None    # Every Element of the List would be the list in itsself where the first index would represent type of Callback Function
                                    # abd rest would represent its configuration params
                                    # Callback Name : type(callback_var).__name__
                                    # Params : callback_var.paramName


    def initiateSessionRequest(self):
        print("\n--------------------------------------------------------------------------------------------------\n")

        if self.allConfigsDone == False:
            print("PLEASE CONFIGURE THE MODEL FIRST !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return
        
        credentialServer_ipAddress = input("Enter the IP Address of the Server : ")  

        connectedToServer = False

        email , password = None , None

        try:
            requestURL = f"http://{credentialServer_ipAddress}:5500/serverRunning"
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
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    connectedToServer = False
                    return 
        except requests.exceptions.ConnectionError:
            print("EITHER SERVER IS NOT RUNNING RIGHT NOW OR THE IP ADDRESS ENTERED IS INCORRECT\nPLEASE CHECK THE ENTERED IP ADDRESS OR ELSE TRY AGAIN LATER")
            print("\n--------------------------------------------------------------------------------------------------\n")
            connectedToServer = False
            return 
        except Exception as error:
            print(f"THE FOLLOWING ERROR OCCURED WHEN CONNECTING TO THE SERVER : {error}")
            print("\n--------------------------------------------------------------------------------------------------\n")
            credentialsVerified = False
            return 

        if(not connectedToServer):
            print("YOUR ARE NOT CONNECTED TO THE SERVER !!")
            print("PLEASE CONNECT TO THE SERVER FIRST !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return
        
        try:
            email = input("Enter Your Account Email Address : ")
            password = input("Enter Your Account Password : ")
            relevantInformation = {"MODEL_JSON" : self.modelJson , "OPTIMIZER_CONFIG" : self.optimizerConfig , "METRICS" : self.metricsList , "LOSS" : self.loss , "LOSS_WEIGHTS" : self.lossWeights , "WEIGHTED_METRICS" : self.weightedMetrics , "EPOCHS" : self.epoch}
            jsMsg = {"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password , "DATA" : relevantInformation}
            requestURL = f"http://{credentialServer_ipAddress}:5500/requestSessionCreation"
            response = requests.post(requestURL , json=jsMsg)
            if response.status_code == 200:
                data = response.json()
                if data['message'] == "Request Submitted":
                    print("THE REQUEST WAS SUBMITTED SUCCESSFULLY !!")
                    print("INITIALIZE YOU SESSION USING YOUR DESKTOP APPLICATION !!")
                    self._sessionCreated = True
                    self._connectedToServer = True
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    return
                else:
                    print(data['message'])
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    return 
            else:
                print("SESSION COULD NOT BE CREATED !!")
                print(response.json()['message'])
                print("\n--------------------------------------------------------------------------------------------------\n")
                return 
        except Exception as error:
            print(f"THE FOLLOWING ERROR OCCURED WHEN CREATING THE SESSION : {error}")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return
        


    def validModelLayers(self , layers):
        for layer in [(str(lay.__class__.__module__)).split('.') for lay in layers]:
            if(layer[0] == 'keras'):
                if(layer[1] == 'layers'):
                    pass
                elif(layer[1] == 'engine'):
                    if(layer[2] == 'input_layer'):
                        pass
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def InformationTransfer(self , model , epochs):
        self.setModel(model)
        self.setEpochs(epochs)
        pass

    def setEpochs(self , epochs):
        if type(epochs) == int:
            self.epoch = epochs
        else:
            print("\n--------------------------------------------------------------------------------------------------\n")
            print("PLEASE ENTER A VALID INTEGER VALUE FOR EPOCHS !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
    

    def setModel(self , model):
        if isinstance(model, keras_models.Sequential) or isinstance(model, keras_models.Model):
            self.modelJson = json.loads(model.to_json())
            if self.validModelLayers(model.layers) == False:
                print("\n--------------------------------------------------------------------------------------------------\n")
                print("INVALID MODEL LAYERS GIVEN !!")
                print("\n--------------------------------------------------------------------------------------------------\n")
                self.allConfigsDone = False
                modelJson = None
                return 
            else:
                print("\n--------------------------------------------------------------------------------------------------\n")
                print("MODEL CONFIGURATIONS HAS BEEN SUCCESSFULLY NOTED DOWN !!")

            if not model.optimizer:
                print("MODEL HAS NO OPTIMIZER")
                print("PLEASE COMPILE THE MODEL BEFORE SENDING THE MODEL")
                print("\n--------------------------------------------------------------------------------------------------\n")
                return
            self.setOptimizer(model.optimizer)
            self.setLoss(model.compiled_loss._user_losses)
            self.setMetrics(model.compiled_metrics._user_metrics)
            self.setLossWeights(model.compiled_loss._user_loss_weights)
            self.setWeightedMetrics(model.compiled_metrics._user_weighted_metrics)
            self.allConfigsDone = True
            print("MODEL OPTIMIZER IS ALSO SUCCESSFULLY NOTED DOWN !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
        else:
            print("\n--------------------------------------------------------------------------------------------------\n")
            print("PASS A VALID MODEL")
            print("\n--------------------------------------------------------------------------------------------------\n")

    def setOptimizer(self , optimizer):
        if optimizer:
            self.optimizerConfig = optimizer.get_config()
    
    def setLoss(self , loss):
        self.loss = loss
    
    def setMetrics(self , metrics):
        self.metricsList = metrics
    
    def setLossWeights(self , lossWeights):
        self.lossWeights = lossWeights
    
    def setWeightedMetrics(self , weightedMetrics):
        self.weightedMetrics = weightedMetrics

    def AllConfigs(self):
        print("Model Json : " , self.modelJson)
        print("Optimizer Config : " , self.optimizerConfig)
        print("Loss : " , self.loss)
        print("Metrics : " , self.metricsList)
        print("Loss Weights : " , self.lossWeights)
        print("Weighted Metrics : " , self.weightedMetrics)
        print("Epochs : " , self.epoch)
    



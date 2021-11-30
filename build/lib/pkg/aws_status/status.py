import boto3, logging
import pkg.utils.client.client as client

class AWS_AZ(object):
    def __init__(self, client=None):
        self.clients = client

    def CheckAWSStatus(self, experimentsDetails):
        
        self.clients = client.AWSClient().clientElb
        
        if experimentsDetails.LoadBalancerName == "" or experimentsDetails.LoadBalancerZones == "" :
            return ValueError("Provided LoadBalancer Name or LoadBalanerZoner are empty")
        
        err = self.checkLBStatus()
        if err != None:
            return err
        logging.info("[Info]: LoadBalancer and Availablity of zone has been checked")
        # err = self.checkAZones(self, experimentsDetails)
        # if err != None:
        #     return err

    def checkLBStatus(self):
        try:
            self.clients.describe_load_balancers()['LoadBalancerDescriptions']
        except Exception as exp:
            return ValueError(exp)

    def detachAZfromLB(self, experimentsDetails, zone): 
        self.clients = client.AWSClient().clientElb 
        try:
            response = self.clients.disable_availability_zones_for_load_balancer(
                LoadBalancerName=experimentsDetails.LoadBalancerName,
                AvailabilityZones=[
                    zone,
                ]
            )
            # return response

        except (self.clients.exceptions.AccessPointNotFoundException, self.clients.exceptions.InvalidConfigurationRequestException) as exp:
            return ValueError(exp)

    def attachAZtoLB(self, experimentsDetails, zone):
        self.clients = client.AWSClient().clientElb
        try:
            response = self.clients.enable_availability_zones_for_load_balancer(
                LoadBalancerName=experimentsDetails.LoadBalancerName,
                AvailabilityZones=[
                    zone,
                ]
            )
            # return response
        except (self.clients.exceptions.AccessPointNotFoundException, self.clients.exceptions.InvalidConfigurationRequestException) as exp:
            return ValueError(exp)

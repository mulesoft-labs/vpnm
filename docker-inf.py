import os, re, logging, requests, json
import configargparse
import logging

logging.basicConfig(level=logging.INFO)

class VpnMigInf:

  def __init__(self, user, password, org_id, vpc_id, action, dryrun='yes'):
    self.user = user
    self.password = password
    self.org_id = org_id
    self.vpc_id = vpc_id
    self.action = action
    self.dryrun = dryrun
    self.__logger = logging.getLogger('vpnm')
    self.bearer_ep = "https://anypoint.mulesoft.com/accounts/login"
    self.vpnm_ep = "https://vpnm.api.env.support.mulesoft.com/cloudhub/api/organizations/{}/vpcs/{}".format(self.org_id, self.vpc_id)


  def get_bearer_token(self):

    try:

      self.__logger.info("Getting the bearer token")
      r=requests.post(self.bearer_ep, data={"username": self.user, "password": self.password })

      # Only proceed with status code 200
      if r.status_code != requests.codes.ok:
        self.__logger.error("{}/{}".format(r.status_code, r.reason))
        self.__logger.error(r.text)
        exit(1)

      
      json_data = json.loads(r.text)
      self.__logger.info(json_data)
      return json_data['access_token']

    except Exception as e:
      self.__logger.error(e)
      exit(1)


  def invoke_api(self, bearer):

    try:
      self.__logger.info("Calling the VPN migration API")
      params={"action":self.action, "dryrun":self.dryrun}
      headers = {'Authorization': 'Bearer {}'.format(bearer)}
      r=requests.post(self.vpnm_ep, headers=headers, params=params)

      if r.status_code != requests.codes.ok:
        self.__logger.error("code: {}, reason: {}".format(r.status_code, r.reason))
        self.__logger.error(r.text)
        exit(1)

      self.__logger.info(r.text)

      return

    except Exception as e:
      self.__logger.error(e)
      exit(1)



if __name__ == "__main__":

  p = configargparse.ArgParser()
  
  p.add('-u', '--user', required=True, help='Anypoint user name')
  p.add('-p', '--password', required=True, help='Anypoint user password')
  p.add('-o', '--org', required=True, help='Anypoint organization ID')
  p.add('-v', '--vpc', required=True, help='CloudHub VPC ID')
  p.add('-a', '--action', choices=['remove', 'restore'], required=True, help="Action only 'remove' or 'restore'")
  p.add('--dryrun', choices=['yes', 'no'], required=False, default='yes', help='Dryrun (yes|no)')

  args = p.parse_args()

  vpnm = VpnMigInf(user=args.user, password=args.password, org_id=args.org, vpc_id=args.vpc, 
    action=args.action, dryrun=args.dryrun)

  bearer = vpnm.get_bearer_token()
  vpnm.invoke_api(bearer)
  


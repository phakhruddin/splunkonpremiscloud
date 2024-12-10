module "splunk" {
  source          = "../../modules/splunk"
  splunk_username = var.splunk_username
  splunk_password = var.splunk_password
  splunk_url      = "https://splunk-dev-instance:8089"

  index_names = ["index1", "index2", "index3"]

  alerts = {
    high_cpu = {
      query = "index=main | stats avg(cpu) by host"
      cron  = "*/5 * * * *"
    },
    disk_space = {
      query = "index=main | stats avg(disk_space) by host"
      cron  = "0 * * * *"
    }
  }
}

provider "splunk" {
  username = var.splunk_username
  password = var.splunk_password
  url      = var.splunk_url
}

# Example: Create Splunk Indexes
resource "splunk_index" "indexes" {
  for_each = toset(var.index_names)

  name       = each.value
  max_size   = var.index_max_size
  home_path  = "/opt/splunk/var/lib/splunk/${each.value}/db"
  cold_path  = "/opt/splunk/var/lib/splunk/${each.value}/colddb"
  thawed_path = "/opt/splunk/var/lib/splunk/${each.value}/thaweddb"

  depends_on = [splunk_server_configuration.main]
}

# Example: Configure Splunk Servers
resource "splunk_server_configuration" "main" {
  stanza = "general"
  settings = {
    enable_ssl = true
  }
}

# Example: Create Alerts
resource "splunk_saved_search" "alerts" {
  for_each = toset(var.alerts)

  name          = each.key
  search_string = each.value.query
  cron_schedule = each.value.cron
  actions = {
    action.email = true
  }
}

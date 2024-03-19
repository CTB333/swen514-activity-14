variable "token" {
  type        = string
  description = "github token to connect github repo"
  default     = "" # "Your Gitub Token"
}

variable "repository" {
  type        = string
  description = "github repo url"
  default     = "" # "YOUR SOURCE-CODE REPO URL"
}

variable "app_name" {
  type        = string
  description = "AWS Amplify App Name"
  default     = "tut-amplify"
}

variable "branch_name" {
  type        = string
  description = "AWS Amplify App Repo Branch Name"
  default     = "master"
}


variable "domain_name" {
  type        = string
  default     = "tut_awsamplifyapp.com"
  description = "AWS Amplify Domain Name"
}
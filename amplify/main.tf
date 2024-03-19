provider "aws" {
    region = "us-east-1"
}

locals {
    aws_key = "PairOneV"   
}

resource "aws_amplify_app" "tut_amplify_app" {
    name = var.app_name
    repository = var.repository
    oauth_token = var.token

    build_spec = "build.yml"
}

resource "aws_amplify_branch" "tut_amplify_branch" {
    app_id = aws_amplify_app.tut_amplify_app.id
    branch_name = var.branch_name
}

resource "aws_amplify_domain_association" "tut_domain_association" {
    app_id = aws_amplify_app.tut_amplify_app.id
    domain_name = var.domain_name
    wait_for_verification = false

    sub_domain {
        branch_name = aws_amplify_branch.tut_amplify_branch.branch_name
        prefix = var.branch_name
    }
}
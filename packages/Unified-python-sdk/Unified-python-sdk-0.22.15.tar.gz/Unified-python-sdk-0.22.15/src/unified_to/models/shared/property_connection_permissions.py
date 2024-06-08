"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
from enum import Enum


class PropertyConnectionPermissions(str, Enum):
    AUTH_LOGIN = 'auth_login'
    ACCOUNTING_ACCOUNT_READ = 'accounting_account_read'
    ACCOUNTING_ACCOUNT_WRITE = 'accounting_account_write'
    ACCOUNTING_TRANSACTION_READ = 'accounting_transaction_read'
    ACCOUNTING_TRANSACTION_WRITE = 'accounting_transaction_write'
    ACCOUNTING_INVOICE_READ = 'accounting_invoice_read'
    ACCOUNTING_INVOICE_WRITE = 'accounting_invoice_write'
    ACCOUNTING_CONTACT_READ = 'accounting_contact_read'
    ACCOUNTING_CONTACT_WRITE = 'accounting_contact_write'
    ACCOUNTING_TAXRATE_READ = 'accounting_taxrate_read'
    ACCOUNTING_TAXRATE_WRITE = 'accounting_taxrate_write'
    ACCOUNTING_ORGANIZATION_READ = 'accounting_organization_read'
    PAYMENT_PAYMENT_READ = 'payment_payment_read'
    PAYMENT_PAYMENT_WRITE = 'payment_payment_write'
    PAYMENT_PAYOUT_READ = 'payment_payout_read'
    PAYMENT_REFUND_READ = 'payment_refund_read'
    PAYMENT_LINK_READ = 'payment_link_read'
    PAYMENT_LINK_WRITE = 'payment_link_write'
    COMMERCE_ITEM_READ = 'commerce_item_read'
    COMMERCE_ITEM_WRITE = 'commerce_item_write'
    COMMERCE_COLLECTION_READ = 'commerce_collection_read'
    COMMERCE_COLLECTION_WRITE = 'commerce_collection_write'
    COMMERCE_INVENTORY_READ = 'commerce_inventory_read'
    COMMERCE_INVENTORY_WRITE = 'commerce_inventory_write'
    COMMERCE_LOCATION_READ = 'commerce_location_read'
    COMMERCE_LOCATION_WRITE = 'commerce_location_write'
    ATS_ACTIVITY_READ = 'ats_activity_read'
    ATS_ACTIVITY_WRITE = 'ats_activity_write'
    ATS_APPLICATION_READ = 'ats_application_read'
    ATS_APPLICATION_WRITE = 'ats_application_write'
    ATS_APPLICATIONSTATUS_READ = 'ats_applicationstatus_read'
    ATS_CANDIDATE_READ = 'ats_candidate_read'
    ATS_CANDIDATE_WRITE = 'ats_candidate_write'
    ATS_INTERVIEW_READ = 'ats_interview_read'
    ATS_INTERVIEW_WRITE = 'ats_interview_write'
    ATS_JOB_READ = 'ats_job_read'
    ATS_JOB_WRITE = 'ats_job_write'
    ATS_COMPANY_READ = 'ats_company_read'
    ATS_DOCUMENT_READ = 'ats_document_read'
    ATS_DOCUMENT_WRITE = 'ats_document_write'
    ATS_SCORECARD_READ = 'ats_scorecard_read'
    ATS_SCORECARD_WRITE = 'ats_scorecard_write'
    CRM_COMPANY_READ = 'crm_company_read'
    CRM_COMPANY_WRITE = 'crm_company_write'
    CRM_CONTACT_READ = 'crm_contact_read'
    CRM_CONTACT_WRITE = 'crm_contact_write'
    CRM_DEAL_READ = 'crm_deal_read'
    CRM_DEAL_WRITE = 'crm_deal_write'
    CRM_EVENT_READ = 'crm_event_read'
    CRM_EVENT_WRITE = 'crm_event_write'
    CRM_LEAD_READ = 'crm_lead_read'
    CRM_LEAD_WRITE = 'crm_lead_write'
    CRM_PIPELINE_READ = 'crm_pipeline_read'
    CRM_PIPELINE_WRITE = 'crm_pipeline_write'
    MARTECH_LIST_READ = 'martech_list_read'
    MARTECH_LIST_WRITE = 'martech_list_write'
    MARTECH_MEMBER_READ = 'martech_member_read'
    MARTECH_MEMBER_WRITE = 'martech_member_write'
    TICKETING_CUSTOMER_READ = 'ticketing_customer_read'
    TICKETING_CUSTOMER_WRITE = 'ticketing_customer_write'
    TICKETING_TICKET_READ = 'ticketing_ticket_read'
    TICKETING_TICKET_WRITE = 'ticketing_ticket_write'
    TICKETING_NOTE_READ = 'ticketing_note_read'
    TICKETING_NOTE_WRITE = 'ticketing_note_write'
    HRIS_EMPLOYEE_READ = 'hris_employee_read'
    HRIS_EMPLOYEE_WRITE = 'hris_employee_write'
    HRIS_GROUP_READ = 'hris_group_read'
    HRIS_GROUP_WRITE = 'hris_group_write'
    HRIS_PAYSLIP_READ = 'hris_payslip_read'
    HRIS_PAYSLIP_WRITE = 'hris_payslip_write'
    HRIS_TIMEOFF_READ = 'hris_timeoff_read'
    HRIS_TIMEOFF_WRITE = 'hris_timeoff_write'
    UC_CALL_READ = 'uc_call_read'
    STORAGE_FILE_READ = 'storage_file_read'
    STORAGE_FILE_WRITE = 'storage_file_write'
    WEBHOOK = 'webhook'
    GENAI_MODEL_READ = 'genai_model_read'
    GENAI_PROMPT_READ = 'genai_prompt_read'
    GENAI_PROMPT_WRITE = 'genai_prompt_write'
    MESSAGING_MESSAGE_READ = 'messaging_message_read'
    MESSAGING_MESSAGE_WRITE = 'messaging_message_write'
    MESSAGING_CHANNEL_READ = 'messaging_channel_read'
    KMS_SPACE_READ = 'kms_space_read'
    KMS_SPACE_WRITE = 'kms_space_write'
    KMS_PAGE_READ = 'kms_page_read'
    KMS_PAGE_WRITE = 'kms_page_write'
    KMS_COMMENT_READ = 'kms_comment_read'
    KMS_COMMENT_WRITE = 'kms_comment_write'
    TASK_PROJECT_READ = 'task_project_read'
    TASK_PROJECT_WRITE = 'task_project_write'
    TASK_TASK_READ = 'task_task_read'
    TASK_TASK_WRITE = 'task_task_write'

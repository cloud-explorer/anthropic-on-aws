class ModelIDs:
    anthropic_claude_3_5_sonnet = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    anthropic_claude_3_sonnet = "anthropic.claude-3-sonnet-20240229-v1:0"
    anthropic_claude_3_opus = "anthropic.claude-3-opus-20240229-v1:0"
    anthropic_claude_3_haiku = "anthropic.claude-3-haiku-20240307-v1:0"

class ToolConfig:
    
    SONNET_35 = "SONNET_35"

    SUMMARY_PROMPT = """
                Provide a comprehensive summary of all entities extracted and actions performed during the loan application processing. 
                The summary should be formatted in markdown and organized into clear sections. For each section, list the extracted 
                entities and their corresponding values. Highlight all extracted values using backticks (`).

                Do not include section that were not requested to be extracted in the original prompt.

                Example of the outout structure is shown below:

                ### Loan Information
                - Loan Amount: `[value]`
                - Loan Purpose: `[value]`
                - Property Address: `[value]`
                - Property Value: `[value]`

                ### Borrower Information
                - Full Name: `[value]`
                - SSN: `[value]`
                - Date of Birth: `[value]`
                - Citizenship: `[value]`
                - Marital Status: `[value]`
                - Current Address: `[value]`
                - Email: `[value]`

                ### Driver's License Information
                - License Number: `[value]`
                - Expiration Date: `[value]`
                - State of Issue: `[value]`
                [Other relevant information]

                ### Employment Information
                - Current Employer: `[value]`
                - Employer Address: `[value]`
                - Start Date: `[value]`

                ### Financial Information
                    #### Assets
                    - [Account Type]: `[value]`
                    - [Institution]: `[value]`
                    - Account Number: `[value]`
                    - Cash/Market Value: `[value]`

                    #### Liabilities
                    - [Account Type]: `[value]`
                    - [Company Name]: `[value]`
                    - Account Number: `[value]`
                    - Unpaid Balance: `[value]`
                    - Monthly Payment: `[value]`

                ### W2 Information
                - Tax Year: `[value]`
                - Employer EIN: `[value]`
                - Wages, Tips, Other Compensation: `[value]`
                - Federal Income Tax Withheld: `[value]`
                - Social Security Wages: `[value]`
                - Medicare Wages and Tips: `[value]`

                ### Declarations
                - [Each declaration question]: `[Yes/No]`

                ### Loan Originator Information
                - Organization Name: `[value]`
                - Originator Name: `[value]`
                - NMLSR ID: `[value]`

                ### Verification Actions
                - [Description of each verification action performed. Highlight the names and values that do not match]

                ### Flags and Discrepancies
                - [List any flags raised or discrepancies found during the process]

                Ensure that all extracted information is included and properly formatted. If any required information is missing 
                or could not be extracted, indicate this with `NOT_FOUND`. For any verification actions or discrepancies, provide 
                a brief explanation of their significance in the loan application process.

                Important Instructions:
                1. Only include sections and information that were specifically requested or extracted in the original process.
                2. Do not create or include sections that were not part of the extraction or verification process.
                3. If a section was requested but no information was found or extracted, include the section heading with a note 
                stating "No information extracted" or "Information not found".
                4. Ensure that all extracted information is properly formatted with values highlighted using backticks (`).
                5. If any required information is missing or could not be extracted, indicate this with `NOT_FOUND`.
                6. For any verification actions or discrepancies, provide a brief explanation of their significance in the loan 
                application process. Also show the mismatched names and other values.
                """
    DOCUMENT_PROCESSING_PIPELINE = [
        {
            "toolSpec": {
                "name": "pdf_to_images",
                "description": """
                This tool converts a PDF file into a series of image files. It should be used when the incoming file 
                is in PDF format and needs to be processed as images. The tool takes a single PDF file path as input 
                and returns an array of file paths for the generated images. Each page of the PDF will be converted 
                into a separate image file. This conversion is crucial for subsequent document analysis and 
                classification tasks that require image input. The tool does not modify the original PDF file.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Path to the input PDF file."
                            }
                        },
                        "required": ["pdf_path"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "classify_documents",
                "description": """
                This tool classifies the documents in a loan application package. It should be used after the PDF 
                has been converted to images. The tool analyzes each document image and categorizes it based on its 
                content and purpose within the loan application process. It can identify various document types such 
                as URLA (Uniform Residential Loan Application), driver's licenses, and other relevant documents. 
                The classification includes a confidence score for each categorization. This tool is essential for 
                organizing and validating the completeness of the loan application package.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of paths to the extracted documents.",
                            }
                        },
                        "required": ["document_paths"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "check_required_documents",
                "description": """
                This tool is always run immediately after the classification of documents. It verifies if all 
                required document types, specifically the URLA (Uniform Residential Loan Application) and Driver's 
                License, are present in the classified documents. The tool analyzes the classification results, 
                checking for the presence of these critical documents. If any required document is missing, it flags 
                the application for potential rejection. This step is crucial in ensuring the completeness of the 
                loan application package before further processing. The tool provides a detailed breakdown of present 
                and missing documents, along with their associated confidence scores and identified topics.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "classified_documents": {
                                "type": "array",
                                "properties": {
                                    "category": {
                                        "type": "string",
                                        "enum": ["URLA", "DRIVERS_LICENSE", "UNK"],
                                        "description": "The category of the document"
                                    },
                                    "file_path": {
                                        "type": "string",
                                        "description": "Path to the files that was classified for this category."
                                    },
                                    "topics": {
                                        "type": "object",
                                        "enum": ["BORROWER_PERSONAL_INFO",
                                                "BORROWER_CURRENT_EMPLOYER", 
                                                "BORROWER_ASSETS", 
                                                "BORROWER_LIABILITIES", 
                                                "LOAN_PROPERTY_INFO", 
                                                "DECLARATIONS", 
                                                "LOAN_ORIGINATOR_INFO", 
                                                "DRIVERS_LICENSE", 
                                                "UNK"],
                                        "description": """
                                        This shows the sections that are included in the document. 
                                        This will be a JSON object (dictionary) 
                                        For example `1a. Personal Information` is on the page this will include `BORROWER_PERSONAL_INFO`, 
                                        if `Loan Originator Information` is on this page, the value will include `LOAN_ORIGINATOR_INFO`. 
                                        Read and understand the document completely. Double check values and entity assocations.
                                        Read the information on the page carefully to understand which topics need to be include from the provided choices.
                                        For example if there is no information about the property loan on a given page, do not include LOAN_PROPERTY_INFO
                                        """
                                    },
                                    "confidence_score": {
                                        "type": "number",
                                        "description": "Confidence score of the classification."
                                    }
                                },
                                "required": ["category", "file_path", "topics", "confidence_score"]
                            }
                        },
                        "required": ["classified_documents"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "reject_incomplete_application",
                "description": """
                This tool is specifically invoked when the check_required_documents tool identifies missing documents 
                in the loan application package. It formalizes the rejection process for incomplete applications. 
                The tool takes a list of missing document types as input and generates a formal rejection notice. 
                This notice typically includes details on which specific documents are missing and instructions for 
                the applicant on how to complete their application. It's a critical step in maintaining the integrity 
                of the loan application process and ensuring all necessary information is collected before proceeding 
                with the loan evaluation.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "missing_documents": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of missing document types. Double check the missing documents list before including here"
                            }
                        },
                        "required": ["missing_documents"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "summarize_session",
                "description": """
                This tool is always run at the end of the document processing pipeline. It provides a comprehensive 
                summary of all actions taken during the current processing session. The summary includes details on 
                each entity extracted and saved, the outcomes of document classification and verification, and any 
                other significant actions or decisions made during the process. If the application was rejected due 
                to missing documents, this will be clearly stated. The tool also notes whether specific guardrails 
                were enabled during the process, as requested by the user. This summary serves as a crucial record 
                for auditing and reviewing the loan application processing workflow.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": f"{SUMMARY_PROMPT}"
                            },
                            "enable_guardrail": {
                                "type": "boolean",
                                "description": """
                                This parameter will be `True` if the user asked for the guardrail to be enabled, 
                                `False` if they did not ask for it to be enabled.
                                """
                            }
                        },
                         "required": ["summary"]
                    }
                }
            }
        }
    ]


    URLA_LOAN_INFO = [
        {
            "toolSpec": {
                "name": "extract_urla_loan_info",
                "description": """
                This tool extracts loan information specifically from 'Section 4: Loan and Property Information' 
                of the Uniform Residential Loan Application (URLA) form. It should be used after the URLA document 
                has been identified and classified. The tool analyzes the relevant sections of the URLA to extract 
                key loan details such as loan amount, purpose, property address, and value. This information is 
                crucial for loan processing and underwriting. The tool is designed to handle variations in URLA 
                format and extract information accurately even if the layout slightly differs across applications.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic BORROWER_PERSONAL_INFO"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_urla_loan_info",
                "description": """
                This tool is responsible for saving the extracted loan information from 'Section 4: Loan and Property 
                Information' of the URLA form into a structured format. It should be used immediately after the 
                extract_urla_loan_info tool. The tool takes the extracted information and saves it in a standardized 
                format, ensuring data consistency and facilitating easy retrieval for further processing. It handles 
                data validation to ensure all required fields are present and correctly formatted. If any required 
                information is missing or seems incorrect, the tool will flag it for review.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "loan_info": {
                                "type": "object",
                                "properties": {
                                    "loan_amount": {"type": "number", "description": "The loan amount requested"},
                                    "loan_purpose": {"type": "string", "enum": ["Purchase", "Refinance", "Other"], "description": "The purpose of the loan"},
                                    "property_address": {"type": "string", "description": "The full address of the property"},
                                    "property_value": {"type": "number", "description": "The value of the property"}
                                },
                                "required": ["loan_amount", "loan_purpose", "property_address"]
                            }
                        },
                        "required": ["loan_info"]
                    }
                }
            }
        }
    ]

    URLA_BORROWER_INFO = [
        {
            "toolSpec": {
                "name": "extract_urla_borrower_info",
                "description": """
                This tool extracts borrower information from 'Section 1: Borrower Information' of the URLA form. 
                It should be used after the URLA document has been identified and classified. The tool carefully 
                analyzes the relevant sections to extract comprehensive borrower details including personal 
                information, contact details, and citizenship status. It's designed to handle various formats of 
                the URLA and can extract information even if the layout differs slightly between applications. 
                The tool is crucial for gathering essential applicant data for loan processing and risk assessment.
                When picking values from radio buttons, pay attention to which value is selected.
                Include within \<thinking>\</thinking> tags the reason why you chose to pick each of the values
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic LOAN_PROPERTY_INFO"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_urla_borrower_info",
                "description": """
                This tool is responsible for saving the extracted borrower information from 'Section 1: Borrower 
                Information' of the URLA form into a structured format. It should be used immediately after the 
                extract_urla_borrower_info tool. The tool takes the extracted information and saves it in a 
                standardized format, ensuring data consistency and facilitating easy retrieval for further 
                processing. It performs data validation to ensure all required fields are present and correctly 
                formatted. The tool also handles sensitive information like SSN with appropriate security measures. 
                If any required information is missing or seems incorrect, the tool will flag it for review.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "borrower_info": {
                                "type": "object",
                                "properties": {
                                    "firstname": {"type": "string", "description": "First name of the borrower"},
                                    "middlename": {"type": "string", "description": "Middle name of the borrower"},
                                    "lastname": {"type": "string", "description": "Last name of the borrower"},
                                    "ssn": {"type": "string", "description": "Social Security Number of the borrower"},
                                    "dob": {"type": "string", "description": "Date of birth of the borrower"},
                                    "citizenship": {"type": "string", "enum": ["U.S. Citizen", "Permanent Resident Alien", "Non-Permanent Resident Alien"], "description": "Citizenship status of the borrower."},
                                    "marital_status": {"type": "string", "enum": ["Married", "Separated", "Unmarried"], "description": "Marital status of the borrower"},
                                    "dependents": {"type": "number", "description": "Number of dependents"},
                                    "current_address": {"type": "string", "description": "Current address of the borrower"},
                                    "email_id": {"type": "string", "description": "Email of the borrower"}
                                },
                                "required": ["name", "ssn", "dob", "citizenship", "marital_status", "current_address", "email_id"]
                            }
                        },
                        "required": ["borrower_info"]
                    }
                }
            }
        }
    ]

    DRIVERS_LICENSE = [
        {
            "toolSpec": {
                "name": "extract_drivers_info",
                "description": """
                This tool extracts detailed information from a driver's license document. It should be used after 
                a document has been classified as a driver's license. The tool uses advanced image processing and 
                OCR techniques to accurately extract all relevant information from the license, including personal 
                details, license specifics, and issuance information. It's designed to handle various formats of 
                driver's licenses from different states and can extract information even if the layout differs. 
                The tool is crucial for verifying the borrower's identity and obtaining accurate personal information.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "dl_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as DRIVERS_LICENSE"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_drivers_info",
                "description": """
                This tool is responsible for saving the extracted information from a driver's license into a 
                structured format. It should be used immediately after the extract_drivers_info tool. The tool 
                takes the extracted information and saves it in a standardized format, ensuring data consistency 
                and facilitating easy retrieval for further processing. It performs data validation to ensure all 
                required fields are present and correctly formatted. The tool also handles sensitive information 
                with appropriate security measures. If any required information is missing or seems incorrect, 
                the tool will flag it for review. This saved information is crucial for identity verification 
                and cross-referencing with other application documents.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "license_info": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string", "description": "First name of the license holder"},
                                    "middle_name": {"type": "string", "description": "Middle name of the license holder"},
                                    "last_name": {"type": "string", "description": "Last name of the license holder"},
                                    "address": {"type": "string", "description": "Current address of the license holder"},
                                    "date_of_birth": {"type": "string", "description": "Date of birth of the license holder"},
                                    "sex": {"type": "string", "enum": ["M", "F", "X"], "description": "Sex of the license holder"},
                                    "license_number": {"type": "string", "description": "The driver's license number"},
                                    "class": {"type": "string", "description": "The class of the driver's license"},
                                    "state": {"type": "string", "description": "The state that issued the license"},
                                    "issue_date": {"type": "string", "description": "The date the license was issued"},
                                    "expiration_date": {"type": "string", "description": "The date the license expires"}
                                },
                                "required": ["full_name", "address", "date_of_birth", "sex", "license_number", "class", "state", "issue_date", "expiration_date"]
                            }
                        },
                        "required": ["license_info"]
                    }
                }
            }
        }
    ]

    DL_VALIDATION = [
        {
            "toolSpec": {
                "name": "validate_drivers_license",
                "description": """
                This tool is used to validate the authenticity and current status of a driver's license. It should 
                be used immediately after the driver's license information has been extracted and saved. The tool 
                performs a series of checks to ensure the license is valid, including verifying the license number 
                format, checking the expiration date, and potentially cross-referencing with state DMV databases 
                (if such an API is available). It's crucial for detecting fraudulent or expired licenses early in 
                the loan application process. The tool will return a detailed validation report, including any 
                discrepancies or red flags found during the validation process. If certain information is missing 
                or cannot be validated, the tool will clearly indicate this in its report.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "description": "Validate the driver's license based on information provided. Do not make up values. Send empty string if a value is not found. ",
                        "properties": {
                            "license_info": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string", "description": "First name of the license holder"},
                                    "middle_name": {"type": "string", "description": "Middle name of the license holder"},
                                    "last_name": {"type": "string", "description": "Last name of the license holder"},
                                    "address": {"type": "string", "description": "Current address of the license holder"},
                                    "date_of_birth": {"type": "string", "description": "Date of birth of the license holder"},
                                    "sex": {"type": "string", "enum": ["M", "F", "X"], "description": "Sex of the license holder"},
                                    "license_number": {"type": "string", "description": "The driver's license number"},
                                    "class": {"type": "string", "description": "The class of the driver's license"},
                                    "state": {"type": "string", "description": "The state that issued the license"},
                                    "issue_date": {"type": "string", "description": "The date the license was issued"},
                                    "expiration_date": {"type": "string", "description": "The date the license expires"}
                                },
                                "required": ["full_name", "address", "date_of_birth", "sex", "license_number", "class", "state", "issue_date", "expiration_date"]
                            }
                        },
                        "required": ["license_info"]
                    }
                }
            }
        }
    ]


    VERIFICATION = [
        {
            "toolSpec": {
                "name": "verify_applicant_info",
                "description": """
                This tool performs a critical cross-verification of applicant information across multiple documents. 
                It compares and detects matches between the Uniform Residential Loan Application (URLA), Driver's 
                License, and W2 form. The tool should be used after information has been extracted from all these 
                documents. It checks for consistency in personal details such as name, date of birth, and address 
                across these documents. Any discrepancies found are flagged for further investigation. This 
                verification is crucial for detecting potential fraud or errors in the application process. The 
                tool provides a detailed report of matches and mismatches, helping to ensure the integrity and 
                accuracy of the loan application information.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "description": "Compare and detect matches between the URLA and Driver's License information. Send empty string if a value is not found. Do not make up values.",
                        "properties": {
                            "borrower_info": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string", "description": "First name of the borrower from URLA"},
                                    "middle_name": {"type": "string", "description": "middle name of the borrower from URLA"},
                                    "last_name": {"type": "string", "description": "Last name of the borrower from URLA"},
                                    "dob": {"type": "string", "description": "Date of birth of the borrower from URLA"},
                                    "address": {"type": "string", "description": "Current address of the borrower from URLA"}
                                },
                                "required": ["first_name", "middle_name", "last_name", "dob", "address"]
                            },
                            "license_info": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string", "description": "First name of the license holder"},
                                    "middle_name": {"type": "string", "description": "middle name of the license holder"},
                                    "last_name": {"type": "string", "description": "last name of the license holder"},
                                    "address": {"type": "string", "description": "Current address of the license holder"},
                                    "date_of_birth": {"type": "string", "description": "Date of birth of the license holder"}
                                },
                                "required": ["first_name", "middle_name", "last_name", "address", "date_of_birth"]
                            },
                            "w2_info": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string", "description": "First name of the employee"},
                                    "middle_name": {"type": "string", "description": "middle name of the employee"},
                                    "last_name": {"type": "string", "description": "last name of the employee"},
                                    "address": {"type": "string", "description": "Current address of the employee"}
                                },
                                "required": ["first_name", "middle_name", "last_name", "address"]
                            }
                        },
                        "required": ["borrower_info", "license_info", "w2_info"]
                    }
                }
            }
        }
    ]

    CURRENT_EMPLOYER = [
        {
            "toolSpec": {
                "name": "extract_current_employer",
                "description": """
                This tool extracts current employer information from Section 1b of the Uniform Residential Loan 
                Application (URLA) form. It should be used after the URLA has been classified and the relevant 
                sections identified. The tool uses advanced text recognition to accurately extract details about 
                the applicant's current employment, including the employer's name, address, and the applicant's 
                start date. This information is crucial for assessing the applicant's employment stability and 
                income reliability. The tool is designed to handle various formats of the URLA and can extract 
                information even if the layout differs slightly between applications.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic BORROWER_CURRENT_EMPLOYER."
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_current_employer",
                "description": """
                This tool is responsible for saving the current employer information extracted from Section 1b of 
                the URLA form. It should be used immediately after the extract_current_employer tool. The tool 
                takes the extracted information and saves it in a standardized format, ensuring data consistency 
                and facilitating easy retrieval for further processing. It performs data validation to ensure all 
                required fields are present and correctly formatted. If any required information is missing or 
                seems incorrect, the tool will flag it for review. This saved information is crucial for verifying 
                employment and income details in the loan application process.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "current_employer": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Name of the current employer"},
                                    "address": {"type": "string", "description": "Address of the current employer"},
                                    "start_date": {"type": "string", "description": "Start date of employment"}
                                },
                                "required": ["name", "address", "start_date"]
                            }
                        },
                        "required": ["current_employer"]
                    }
                }
            }
        }
    ]

    ASSETS = [
        {
            "toolSpec": {
                "name": "extract_assets",
                "description": """
                This tool extracts asset information from Section 2a of the Uniform Residential Loan Application 
                (URLA) form. It should be used after the URLA has been classified and the relevant sections 
                identified. The tool uses advanced text recognition to accurately extract details about the 
                applicant's assets, including various types of accounts, financial institutions, account numbers, 
                and their respective cash or market values. This information is crucial for assessing the 
                applicant's financial stability and ability to repay the loan. The tool is designed to handle 
                various formats of the URLA and can extract information even if the layout differs slightly 
                between applications.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic BORROWER_ASSETS."
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_assets",
                "description": """
                This tool is responsible for saving the asset information extracted from Section 2a of the URLA 
                form. It should be used immediately after the extract_assets tool. The tool takes the extracted 
                information and saves it in a standardized format, ensuring data consistency and facilitating 
                easy retrieval for further processing. It performs data validation to ensure all required fields 
                are present and correctly formatted. The tool can handle multiple asset entries, organizing them 
                into an array for easy analysis. If any required information is missing or seems incorrect, the 
                tool will flag it for review. This saved information is crucial for assessing the applicant's 
                financial health and loan eligibility.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "assets": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "account_type": {"type": "string", "description": "Type of account"},
                                        "institution": {"type": "string", "description": "Financial institution"},
                                        "account_number": {"type": "string", "description": "Account number"},
                                        "cash_or_market_value": {"type": "number", "description": "Cash or market value of the asset"}
                                    },
                                    "required": ["account_type", "institution", "account_number", "cash_or_market_value"]
                                }
                            }
                        },
                        "required": ["assets"]
                    }
                }
            }
        }
    ]

    LIABILITIES = [
        {
            "toolSpec": {
                "name": "extract_liabilities",
                "description": """
                This tool extracts liability information from Section 2c of the Uniform Residential Loan 
                Application (URLA) form. It should be used after the URLA has been classified and the relevant 
                sections identified. The tool uses advanced text recognition to accurately extract details about 
                the applicant's liabilities, including various types of debts, creditors, account numbers, unpaid 
                balances, and monthly payments. This information is crucial for assessing the applicant's debt 
                obligations and their ability to take on additional debt. The tool is designed to handle various 
                formats of the URLA and can extract information even if the layout differs slightly between 
                applications.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic BORROWER_LIABILITIES"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_liabilities",
                "description": """
                This tool is responsible for saving the liability information extracted from Section 2c of the 
                URLA form. It should be used immediately after the extract_liabilities tool. The tool takes the 
                extracted information and saves it in a standardized format, ensuring data consistency and 
                facilitating easy retrieval for further processing. It performs data validation to ensure all 
                required fields are present and correctly formatted. The tool can handle multiple liability 
                entries, organizing them into an array for easy analysis. If any required information is missing 
                or seems incorrect, the tool will flag it for review. This saved information is crucial for 
                calculating the applicant's debt-to-income ratio and overall creditworthiness.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "liabilities": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "account_type": {"type": "string", "description": "Type of account"},
                                        "company_name": {"type": "string", "description": "Company name"},
                                        "account_number": {"type": "string", "description": "Account number"},
                                        "unpaid_balance": {"type": "number", "description": "Unpaid balance"},
                                        "monthly_payment": {"type": "number", "description": "Monthly payment"}
                                    },
                                    "required": ["account_type", "company_name", "account_number", "unpaid_balance", "monthly_payment"]
                                }
                            }
                        },
                        "required": ["liabilities"]
                    }
                }
            }
        }
    ]

    DECLARATIONS = [
        {
            "toolSpec": {
                "name": "extract_declarations",
                "description": """
                This tool extracts critical declaration information from Sections 5a and 5b of the Uniform Residential 
                Loan Application (URLA) form. It should be used after the URLA has been classified and relevant sections 
                identified. The tool employs advanced text recognition to accurately extract the applicant's responses 
                to various declarations about their financial and legal status. These declarations cover a wide range 
                of topics including property ownership, business affiliations, undisclosed debts, legal issues, and 
                bankruptcy history. This information is crucial for assessing potential risks associated with the loan 
                application and ensuring compliance with lending regulations. The tool is designed to handle various 
                formats of the URLA and can extract information even if the layout differs slightly between applications.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic DECLARATIONS"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_declarations",
                "description": """
                This tool is responsible for saving the declaration information extracted from Sections 5a and 5b of 
                the URLA form. It should be used immediately after the extract_declarations tool. The tool takes the 
                extracted information and saves it in a standardized format, ensuring data consistency and facilitating 
                easy retrieval for further processing. It performs data validation to ensure all required fields are 
                present and correctly formatted. The tool saves the applicant's responses as boolean values for easy 
                analysis, with an additional field for bankruptcy type if applicable. If any required information is 
                missing or seems incorrect, the tool will flag it for review. This saved information is crucial for 
                identifying potential red flags in the loan application, assessing the applicant's financial history, 
                and ensuring compliance with lending regulations and risk assessment protocols.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "declarations": {
                                "type": "object",
                                "properties": {
                                    "primary_residence": {"type": "boolean", "description": "Will the property be occupied as a primary residence?"},
                                    "business_affiliation": {"type": "boolean", "description": "Does the borrower have a business affiliation with the seller?"},
                                    "other_money_sources": {"type": "boolean", "description": "Is the borrower obtaining money from other sources not disclosed?"},
                                    "other_mortgage_loans": {"type": "boolean", "description": "Does the borrower have other mortgage loans not disclosed?"},
                                    "priority_liens": {"type": "boolean", "description": "Will there be any liens that could take priority over the first mortgage?"},
                                    "co_signer": {"type": "boolean", "description": "Is the borrower a co-signer or guarantor on any undisclosed debt?"},
                                    "outstanding_judgments": {"type": "boolean", "description": "Are there any outstanding judgments against the borrower?"},
                                    "federal_debt_delinquency": {"type": "boolean", "description": "Is the borrower currently delinquent or in default on a Federal debt?"},
                                    "party_to_lawsuit": {"type": "boolean", "description": "Is the borrower a party to a lawsuit with potential financial liability?"},
                                    "property_foreclosure": {"type": "boolean", "description": "Has the borrower conveyed title to a property in lieu of foreclosure in the past 7 years?"},
                                    "pre_foreclosure_sale": {"type": "boolean", "description": "Has the borrower completed a pre-foreclosure sale or short sale in the past 7 years?"},
                                    "property_foreclosed": {"type": "boolean", "description": "Has the borrower had a property foreclosed upon in the last 7 years?"},
                                    "bankruptcy": {"type": "boolean", "description": "Has the borrower declared bankruptcy within the past 7 years?"},
                                    "bankruptcy_type": {"type": "string", "description": "If the borrower declared bankruptcy, what type?"}
                                },
                                "required": ["primary_residence", "business_affiliation", "other_money_sources", "other_mortgage_loans", "priority_liens", "co_signer", "outstanding_judgments", "federal_debt_delinquency", "party_to_lawsuit", "property_foreclosure", "pre_foreclosure_sale", "property_foreclosed", "bankruptcy"]
                            }
                        },
                        "required": ["declarations"]
                    }
                }
            }
        }
    ]

    LOAN_ORIGINATOR = [
        {
            "toolSpec": {
                "name": "extract_loan_originator_info",
                "description": """
                This tool extracts loan originator information from Section 9 of the Uniform Residential Loan 
                Application (URLA) form. It should be used after the URLA has been classified and relevant sections 
                identified. The tool employs advanced text recognition to accurately extract details about both the 
                loan originator organization and the individual loan originator. This information is crucial for 
                regulatory compliance and maintaining a clear record of who processed the loan application. The tool 
                is designed to handle various formats of the URLA and can extract information even if the layout 
                differs slightly between applications. It captures key details such as names, addresses, NMLSR IDs, 
                and contact information.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "urla_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as URLA and contained the topic LOAN_ORIGINATOR_INFO"
                            }
                        }
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_loan_originator_info",
                "description": """
                This tool is responsible for saving the loan originator information extracted from Section 9 of the 
                URLA form. It should be used immediately after the extract_loan_originator_info tool. The tool takes 
                the extracted information and saves it in a standardized format, ensuring data consistency and 
                facilitating easy retrieval for further processing and compliance checks. It performs data validation 
                to ensure all required fields are present and correctly formatted, including checking the format of 
                NMLSR IDs, email addresses, and phone numbers. If any required information is missing or seems 
                incorrect, the tool will flag it for review. This saved information is crucial for maintaining 
                accurate records of loan origination, supporting audit trails, and ensuring compliance with 
                regulatory requirements in the mortgage industry.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "loan_originator": {
                                "type": "object",
                                "properties": {
                                    "organization_name": {"type": "string", "description": "Name of the loan originator organization"},
                                    "organization_address": {"type": "string", "description": "Address of the loan originator organization"},
                                    "organization_nmlsr_id": {"type": "string", "description": "NMLSR ID of the loan originator organization"},
                                    "originator_name": {"type": "string", "description": "Name of the loan originator"},
                                    "originator_nmlsr_id": {"type": "string", "description": "NMLSR ID of the loan originator"},
                                    "originator_email": {"type": "string", "description": "Email of the loan originator"},
                                    "originator_phone": {"type": "string", "description": "Phone number of the loan originator"}
                                },
                                "required": ["organization_name", "organization_address", "organization_nmlsr_id", "originator_name", "originator_nmlsr_id", "originator_email", "originator_phone"]
                            }
                        },
                        "required": ["loan_originator"]
                    }
                }
            }
        }
    ]

    W2_INFO = [
        {
            "toolSpec": {
                "name": "extract_w2_info",
                "description": """
                This tool extracts detailed information from a W2 form, which is a crucial document for verifying 
                an applicant's employment and income. It should be used after the W2 form has been identified and 
                classified. The tool employs advanced optical character recognition (OCR) and machine learning 
                techniques, specifically using the SONNET_35 model, to accurately extract all relevant information 
                from the W2 form. This includes personal details, employer information, and various financial figures. 
                The tool is designed to handle different formats of W2 forms across multiple tax years and can extract 
                information even if the layout varies. This extraction is vital for income verification and fraud 
                detection in the loan application process.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "w2_document_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to the files that were classified as W2"
                            },
                            "model_to_use": {
                                "type": "string", 
                                "description": f"Model to use for extraction. This is always a hard-code value of {SONNET_35}"
                            }
                        },
                        "required": ["w2_document_paths", "model_to_use"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "save_w2_info",
                "description": """
                This tool is responsible for saving the information extracted from a W2 form. It should be used 
                immediately after the extract_w2_info tool. The tool takes the extracted information and saves it 
                in a standardized format, ensuring data consistency and facilitating easy retrieval for further 
                processing and analysis. It performs rigorous data validation to ensure all required fields are 
                present and correctly formatted, including checking the format of tax identification numbers and 
                ensuring numerical values are within expected ranges. The tool is designed to handle sensitive 
                information like SSNs with appropriate security measures. If any required information is missing 
                or cannot be confidently extracted, the tool will return 'NOT_FOUND' for that field rather than 
                making assumptions. This approach ensures the integrity and reliability of the saved data, which 
                is crucial for accurate income verification and fraud prevention in the loan application process.
                """,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "w2_info": {
                                "type": "object",
                                "properties": {
                                    "tax_year": {
                                        "type": "integer",
                                        "description": "The tax year for this W2"
                                    },
                                    "employer_ein": {
                                        "type": "string",
                                        "description": "Employer's Identification Number"
                                    },
                                    "employer_name": {
                                        "type": "string",
                                        "description": "Employer's name"
                                    },
                                    "employer_address": {
                                        "type": "string",
                                        "description": "Employer's address"
                                    },
                                    "employee_ssn": {
                                        "type": "string",
                                        "description": "Employee's Social Security Number"
                                    },
                                    "first_name": {
                                        "type": "string",
                                        "description": "Employee's first name"
                                    },
                                    "employee_middle_name": {
                                        "type": "string",
                                        "description": "Employee's middle name"
                                    },
                                    "employee_last_name": {
                                        "type": "string",
                                        "description": "Employee's last name"
                                    },
                                    "employee_address": {
                                        "type": "string",
                                        "description": "Employee's address"
                                    },
                                    "wages_tips_other_compensation": {
                                        "type": "number",
                                        "description": "Wages, tips, other compensation (Box 1)"
                                    },
                                    "federal_income_tax_withheld": {
                                        "type": "number",
                                        "description": "Federal income tax withheld (Box 2)"
                                    },
                                    "social_security_wages": {
                                        "type": "number",
                                        "description": "Social security wages (Box 3)"
                                    },
                                    "social_security_tax_withheld": {
                                        "type": "number",
                                        "description": "Social security tax withheld (Box 4)"
                                    },
                                    "medicare_wages_and_tips": {
                                        "type": "number",
                                        "description": "Medicare wages and tips (Box 5)"
                                    },
                                    "medicare_tax_withheld": {
                                        "type": "number",
                                        "description": "Medicare tax withheld (Box 6)"
                                    }
                                },
                                "required": [
                                    "tax_year",
                                    "employer_ein",
                                    "employer_name",
                                    "employer_address",
                                    "employee_ssn",
                                    "employee_name",
                                    "employee_address",
                                    "wages_tips_other_compensation",
                                    "federal_income_tax_withheld",
                                    "social_security_wages",
                                    "social_security_tax_withheld",
                                    "medicare_wages_and_tips",
                                    "medicare_tax_withheld"
                                ]
                            }
                        },
                        "required": ["w2_info"]
                    }
                }
            }
        }
    ]


    @classmethod
    def compose_toolspec(cls, *components):
        composed_toolspec = []
        for component in components:
            component_specs = getattr(cls, component, [])
            if isinstance(component_specs, list):
                for spec in component_specs:
                    composed_toolspec.append(spec)
            else:
                composed_toolspec.append(component_specs)
        return composed_toolspec

# Example usage:

"""
full_toolspec = ToolConfig.compose_toolspec(
    'COT', 
    'URLA_LOAN_INFO_TOOL', 
    'URLA_BORROWER_INFO_TOOL', 
    'DRIVERS_LICENSE_TOOL', 
    'VERIFICATION_TOOL',
    'CURRENT_EMPLOYER_TOOL',
    'ASSETS_TOOL',
    'LIABILITIES_TOOL',
    'DECLARATIONS_TOOL',
    'LOAN_ORIGINATOR_TOOL'
)
"""
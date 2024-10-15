from datetime import datetime

class MatchDetector:
    def verify_applicant_info(self, input_data):
        """Compare and detect matches between the URLA (Uniform Residential Loan Application), 
        Driver's License, and W2 information."""
        borrower_info = input_data.get('borrower_info', {})
        license_info = input_data.get('license_info', {})
        w2_info = input_data.get('w2_info', {})
        return self.detect_match(borrower_info, license_info, w2_info)

    def detect_match(self, borrower_info, license_info, w2_info):
        """
        Detect matches between borrower information, license information, and W2 information.
        """
        result = {
            "matches": {
                "first_name": False,
                "middle_name": False,
                "last_name": False,
                "dob": False,
                "address": False,
                "ssn": False
            },
            "discrepancies": [],
            "match_score": 0
        }
    
        self.compare_names(borrower_info, license_info, w2_info, result)
        self.compare_dob(borrower_info, license_info, result)
        self.compare_addresses(borrower_info, license_info, result)
        self.compare_ssn(borrower_info, w2_info, result)
    
        result['match_score'] = (
            (result['matches']['first_name'] * 20) +
            (result['matches']['last_name'] * 20) +
            (result['matches']['dob'] * 20) +
            (result['matches']['address'] * 20) +
            (result['matches']['ssn'] * 20)
        )
    
        return result

    def compare_names(self, borrower_info, license_info, w2_info, result):
        for name_part in ['first_name', 'last_name']:
            urla_name = borrower_info.get(name_part, '').lower()
            license_name = license_info.get(name_part, '').lower()
            w2_name = w2_info.get(name_part, '').lower()
            
            names = [n for n in [urla_name, license_name, w2_name] if n]
            result['matches'][name_part] = len(set(names)) == 1 and len(names) > 1
            if not result['matches'][name_part]:
                result['discrepancies'].append(f"{name_part.replace('_', ' ').title()}")

    def compare_dob(self, borrower_info, license_info, result):
        urla_dob = borrower_info.get('dob')
        license_dob = license_info.get('date_of_birth')
        
        if urla_dob and license_dob:
            try:
                urla_dob = self.parse_date(urla_dob)
                license_dob = self.parse_date(license_dob)
                result['matches']['dob'] = urla_dob == license_dob
                if not result['matches']['dob']:
                    result['discrepancies'].append("Date of Birth")
            except ValueError:
                result['discrepancies'].append("Date of Birth (Invalid format)")
        else:
            result['discrepancies'].append("Date of Birth (Missing)")

    def compare_addresses(self, borrower_info, license_info, result):
        urla_address = borrower_info.get('address', '').lower().replace(' ', '')
        license_address = license_info.get('address', '').lower().replace(' ', '')
        
        if urla_address and license_address:
            address_similarity = self.calculate_similarity(urla_address, license_address)
            result['matches']['address'] = address_similarity >= 0.9
            if not result['matches']['address']:
                result['discrepancies'].append("Address")
        else:
            result['discrepancies'].append("Address (Missing)")

    def compare_ssn(self, borrower_info, w2_info, result):
        urla_ssn = borrower_info.get('ssn', '')
        w2_ssn = w2_info.get('ssn', '')
        
        if urla_ssn and w2_ssn:
            result['matches']['ssn'] = urla_ssn == w2_ssn
            if not result['matches']['ssn']:
                result['discrepancies'].append("SSN")
        else:
            result['discrepancies'].append("SSN (Missing)")

    @staticmethod
    def parse_date(date_string):
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_string}")

    @staticmethod
    def calculate_similarity(str1, str2):
        return sum(a == b for a, b in zip(str1, str2)) / max(len(str1), len(str2))

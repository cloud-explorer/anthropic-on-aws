from datetime import datetime

class DLValidator:
    def validate_drivers_license(self, input_data):
        """
        Validate drivers license information against a set of rules.
        This is a placeholder for the actual validation logic.
        """
        
        license_info = input_data.get('license_info', {})
        if(not license_info):
            return "No license information provided."
        first_name = license_info.get('first_name', '').strip()
        last_name = license_info.get('last_name', '').strip()
        license_number = license_info.get('license_number', '').strip()
        expiration_date = license_info.get('expiration_date', '').strip()

        if(expiration_date < datetime.now().strftime('%Y-%m-%d')):
            return {
                "status": "expired",
                "message": f"Drivers license {license_number} for {first_name} {last_name} has expired on {expiration_date}."
            }
        else:
            return {
                "status": "valid",
                "message": f"Drivers license {license_number} for {first_name} {last_name} is valid until {expiration_date}."
            }
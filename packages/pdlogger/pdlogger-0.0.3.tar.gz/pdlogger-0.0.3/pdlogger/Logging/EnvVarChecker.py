import os

class EnvVarChecker:
    # Define the required environment variables
    REQUIRED_ENV_VARS = [
        'AMQP_URL',
        'QUEUE_NAME',
        'SQL_HOST',
        'SQL_USER',
        'SQL_PASSWORD',
        'SQL_DATABASE'
    ]

    @classmethod
    def check_env_vars(cls):
        """
        Check if all necessary environment variables are initialized.
        Returns a dictionary with variable names and their status (True if set, False otherwise).
        """
        status = {}
        for var in cls.REQUIRED_ENV_VARS:
            status[var] = os.getenv(var) is not None
        return status

    @classmethod
    def all_vars_set(cls):
        """
        Check if all necessary environment variables are initialized.
        Returns True if all are set, False otherwise.
        """
        return all(cls.check_env_vars().values())

# Usage
checker = EnvVarChecker()
env_status = checker.check_env_vars()
all_set = checker.all_vars_set()

print("Environment Variables Status:", env_status)
print("All necessary environment variables are set:", all_set)

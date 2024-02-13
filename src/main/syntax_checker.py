from pylint.lint import Run
from io import StringIO  
import sys

class Syntax_Checker:
    """
    Class for doing a static syntax check on all code in the project
    
    
    methods:
    do_syntax_check(path): runs pylint on the code in the given path, only checking for errors
    do_additional_check(path): runs pylint on the code in the given path
    """

    def __init__(self):
        self.message = ""



    def do_syntax_check(self,path):
        """
        Runs pylint on the code in the given path, 
        only checking for errors.

        Parameters
        ----------
        path: str
            path of files to be checked
        """
        ## Output: Sets message about syntax check status

        output = StringIO()  # Captures output from stdout
        old_stdout = sys.stdout
        sys.stdout = output
       
        try:
            report_format = "--msg-template='{C}:{line:3d},{column}: {obj}: {msg}'" # Sets format for pylint report
            only_errors = "--disable=R,C,W" # Only checks for errors

            result = Run([path,only_errors,report_format],do_exit=False)

            errors = result.linter.stats.by_msg.get('syntax-error', 0)

            if errors == 0:
                self.message += "The code passed the check with no syntax errors \n\n"
                self.do_additional_check(path)  # Does additional checks for warnings
            else:
                self.message += "The code contains syntax errors. \n\n"

            # Formats output
            text = output.getvalue()

        finally:
            sys.stdout = old_stdout
            output.close()

        parts = text.split("------------------------------------------------------------------")
        
        if len(parts) <=2:
            self.message += parts[0]
        
        else:
            warnings = parts[-2].split("\n\n*")
            if len(warnings) >= 2:
                self.message += warnings[1]

    def do_additional_check(self,path):
        """
        Runs pylint on the code in the given path.

        Parameters
        ----------
        path: str
            path of files to be checked
        """
        ## Output: Does another round of checks on the code

        report_format = "--msg-template='{C}:{line:3d},{column}: {obj}: {msg}'"
        Run([path,report_format],do_exit=False)

        self.message += "The following warnings and comments were found for the code \n"

from Search.Receiver_Search import Start_Search 
from SoftwareReceiver_Software import Start_Software


def Decision_Module (Choice) :
    """
    

    Parameters
    ----------
    Choice : String
        Select the command send for the assistant
        Command available :
            
            ----------
            Software
            Search
            ----------
            
    Returns
    -------
    None.

    """
    
    match Choice:
        #Return the correct Logic Method to use in function of what vocal command received
        case "Software":
            Start_Software()
        case "Search":
            Start_Search()
import json

from database_mysql_local.connector import Connector
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerLocal import Logger

from .Constants import (COMMUNICATION_TYPE, DIALOG_WORKFLOW_CODE_LOGGER_OBJECT,
                        CommunicationTypeEnum, WorkflowActionEnum)

logger = Logger.create_logger(object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT)

# from circles_local_aws_s3_storage_python.AWSStorage import AwsS3Storage

# TODO:Let's move to Object Oriented Programming
DEFAULT_STATE_ID = 1


def process_message(communication_type: CommunicationTypeEnum, action_type: WorkflowActionEnum,
                    message: str) -> str or json:
    """Processes message according to which communication_type is used: console or websocket
        If console then we continue the code normally.
        If websocket then we create a json out of the given message and exit(0)"""
    logger.start(object={'communication_type': communication_type, 'action_type': action_type, 'message': message})
    if communication_type == CommunicationTypeEnum.CONSOLE:
        message = message.replace('~', '\n')
    elif communication_type == CommunicationTypeEnum.WEBSOCKET:
        message = update_json_message(action_type, message)
    logger.end(object={'message': message})
    return message


def update_json_message(action_type: WorkflowActionEnum, message: str) -> json:
    """Update message to json format"""
    logger.start(object={"action_type": action_type, "message": message})
    dict_message = {"message": message}
    if action_type == WorkflowActionEnum.AGE_DETECTION:
        dict_message["type"] = "command"
    else:
        dict_message["type"] = "text"
    json_message = json.dumps(dict_message)
    logger.end(object={'json_message': json_message})
    return json_message


def get_curr_state(profile_id: int, channel_id: int = None, campaign_id: int = None) -> int:
    """Returns profiles' curernt state number"""
    logger.start(object={'profile_id': profile_id})
    crud = GenericCRUD(default_schema_name='campaign_channel_profile',
                       default_view_table_name='campaign_channel_profile_view')
    select_clause_value = "last_dialog_workflow_state_id"
    where = "profile_id = %s"
    params = (profile_id,)
    if channel_id:
        where += " AND channel_id = %s"
        params += (channel_id,)
    if campaign_id:
        where += " AND campaign_id = %s"
        params += (campaign_id,)
    curr_state = crud.select_one_value_by_where(where=where, params=params, select_clause_value=select_clause_value)
    if not curr_state:
        curr_state = get_state_id_by_campaign_id(campaign_id)
        if not curr_state:
            curr_state = DEFAULT_STATE_ID
            logger.warning("No state found for the given campaign_id, using default state",
                           object=locals())
    logger.end(object={'curr_state': curr_state})
    return curr_state


def get_state_id_by_campaign_id(campaign_id: int) -> int:
    logger.start(object={'campaign_id': campaign_id})
    crud = GenericCRUD(default_schema_name='campaign', default_view_table_name='campaign_general_view')
    start_state_id = crud.select_one_value_by_column_and_value(
        select_clause_value="start_state_id", column_name="campaign_id", column_value=campaign_id)
    logger.end(object={'start_state_id': start_state_id})
    return start_state_id


def update_profile_curr_state_in_db(new_state: int, profile_id: int,
                                    channel_id: int = None, campaign_id: int = None) -> None:
    """This function updates the last_dialog_workflow_state_id in campaign_channel_profile to the new state.
       Note that this function UPDATES the field and doesn't INSERT into the table. """
    logger.start(object={"new_state": new_state, 'profile_id': profile_id, 'channel_id': channel_id})
    crud = GenericCRUD(default_schema_name='campaign_channel_profile',
                       default_view_table_name='campaign_channel_profile_view')
    where = "profile_id = %s"
    params = (profile_id,)
    if channel_id:
        where += " AND channel_id = %s"
        params += (channel_id,)
    if campaign_id:
        where += " AND campaign_id = %s"
        params += (campaign_id,)
    crud.update_by_where(where=where, params=params, data_dict={"last_dialog_workflow_state_id": new_state})
    logger.end()


# TODO: Make sure we have good testing coverage to this function
def store_age_detection_picture(age_range: str, profile_id: int) -> None:
    """Stores the picture in Nir's storage schema, gets a storage_id and inserts into the computer_vision_storage_table"""
    # storage = AwsS3Storage(bucket_name="storage.us-east-1.dvlp1.bubblez.life", region="us-east-1")
    # storage_id = storage.upload_file("C:\\Users\\User\\OneDrive\\Circles\\age-detection-backend\\src\\alonPicture.png", "Alon's picture", "", 1)

    # age_range_split = age_range.split('-')
    # TODO Why this is commented?
    # TODO Why we commented this? Let's uncomment
    # min_age = int(age_range_split[0][:len(age_range_split[0])-1])
    # max_age = int((age_range_split[1])[1:])
    # cursor.execute("""USE computer_vision_storage""")
    # cursor.execute("""INSERT INTO computer_vision_storage_table
    #                 (storage_id, profile_id, min_age, max_age) VALUES (%s, %s, %s, %s)""",
    #                [storage_id, profile_id, min_age, max_age])
    # connection.commit()
    pass


def get_child_nodes_of_current_state(fields: list, table_name: str, values_from_where_to_select: tuple,
                                     variables_from_where_to_select: list) -> list[dict]:
    """Recieves all the relevant information and selects the child nodes of the current state from the given table, and returns them"""
    logger.start(
        object={'fields': fields, 'table_name': table_name, 'values_from_where_to_select': values_from_where_to_select,
                'variables_from_where_to_select': variables_from_where_to_select})

    crud = GenericCRUD(default_schema_name='dialog_workflow', default_table_name=table_name)
    select_clause_value = ", ".join(fields)
    where = " AND ".join(f"{variable} = %s" for variable in variables_from_where_to_select)
    child_nodes = crud.select_multi_dict_by_where(select_clause_value=select_clause_value,
                                                  where=where, params=values_from_where_to_select)
    # cursor.execute(sql_query, values_from_where_to_select)
    # child_nodes = cursor.fetchall()
    logger.end(object={'child_nodes': child_nodes})
    return child_nodes


class Group:
    def __init__(self, parameter1: int) -> None:
        self.parameter1 = parameter1

    # TODO Make sure we have tests for this and all other methods        
    def get_group_childs_id_bellow_parent_id(self) -> list[int]:
        """returns all the childs ids below the given parent_id.
            This function gets all the id's of records that their parent_state_id is the given id, and continues to add id's  recursively 
            until all the records that their parent_state_id matches an id in the table."""
        logger.start()
        connection = Connector.connect("group")
        cursor = connection.cursor(dictionary=True, buffered=True)
        # TODO Fix this SQL  [why?]
        cursor.execute("""
        WITH RECURSIVE cte AS (
            SELECT group_view.group_id FROM group_view WHERE group_id = %s
            UNION ALL
            SELECT group_view.group_id FROM group_view 
            JOIN cte ON group_view.parent_group_id = cte.group_id
        )
        SELECT cte.group_id FROM cte""", (self.parameter1,))
        group_id_dict = cursor.fetchall()
        group_childs_id = [group['group_id'] for group in group_id_dict]
        logger.end(object={'group_childs_id': group_childs_id})
        return group_childs_id

    def get_child_group_names(self) -> list:
        """Gets all the child title names from the ml table of the given parent_id."""
        logger.start()
        group_ids = self.get_group_childs_id_bellow_parent_id()
        crud = GenericCRUD(default_schema_name='group', default_view_table_name='group_ml_view')
        select_clause_value = "title"
        group_id_placeholders = ','.join(["%s"] * len(group_ids))
        params = tuple(group_ids)
        where = f"group_id IN ({group_id_placeholders})"
        child_group_names = crud.select_multi_value_by_where(select_clause_value=select_clause_value,
                                                             where=where, params=params)
        # child_group_names = [group['title'] for group in group_name_dict]
        logger.end(object={'child_group_names': child_group_names})
        return child_group_names

    # def get_child_group_id(self) -> list[int]:
    #     """Gets the id of all the records with the given group name"""
    #     cursor.execute("""USE `group`""")
    #     cursor.execute("""SELECT group_id from group_ml_en_view WHERE title = %s""", [self.parameter1])
    #     group_id_dict = cursor.fetchall()
    #     return [group['group_id'] for group in group_id_dict]        


# TODO Shall we move this to a menu class?
def generic_menu(*, options: list, got_response: bool, chosen_numbers: str, choose_one_option: bool,
                 outgoing_message: str) -> list[int] or json:
    """A generic function for displaying a menu for the user.
        Returns: If not got_response: the menu options as json to send to user.
                 Otherwise, returns the chosen numbers as list in int"""
    logger.start(object={'options': options, 'got_response': got_response, 'chosen_numbers': chosen_numbers,
                         'choose_one_option': choose_one_option, 'outgoing_message': outgoing_message})
    if not got_response:
        outgoing_message += f"Please choose EXACTLY ONE option between 1-{len(options)}:~" if choose_one_option else f"Please select your desired choices, You may select any of the numbers between 1-{len(options)} with a comma seperator between each choice:~"
        outgoing_message_json = None
        for i, option in enumerate(options):
            outgoing_message = outgoing_message + f'{i + 1}) {option}~'
            outgoing_message_json = process_message(communication_type=COMMUNICATION_TYPE,
                                                    action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
                                                    message=outgoing_message)
        if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
            return outgoing_message_json

    if not chosen_numbers and COMMUNICATION_TYPE == CommunicationTypeEnum.CONSOLE:
        chosen_numbers = input(f"Please choose the options you want between 1-{len(options)}: ")
    chosen_numbers = chosen_numbers.split(',')
    generic_menu_result = [int(x) - 1 for x in chosen_numbers]
    logger.end(object={'generic_menu_result': generic_menu_result})
    return generic_menu_result

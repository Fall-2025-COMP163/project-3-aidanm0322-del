"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)


import character_manager


# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]

    character.setdefault('active_quests', [])
    character.setdefault('completed_quests', [])
    
    #Makes sure the quest isnt completed 
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")
    
    #Makes Sure the level Requirments meet the standard for the quest 
    requried_level = quest.get('required_level', 1)
    if character.get('level', 1) < requried_level:
        raise InsufficientLevelError(f"Character level needs to be at least {requried_level} to accept this quest.")
    
    # Check if the prerequisite quest is completed
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE' and prerequisite not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prerequisite}' not completed.")
    
    #Makes sure quest is not already active
    if quest_id in character['active_quests']:
        return False  # Already active
    
    character['active_quests'].append(quest_id)
    return True

    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    #Check if the quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]

    #Ai helped me with this part due to struggling with it
    character["experience"] = character.get("experience", 0) + quest.get("reward_xp", 0)
    character["gold"] = character.get("gold", 0) + quest.get("reward_gold", 0)



    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    return f"Completed Quest '{quest_id}' successfully"
        


    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """

    character.setdefault('active_quests', [])
    
    #checks if the quest is active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character['active_quests'].remove(quest_id)
    return True
    # TODO: Implement quest abandonment
    

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """

    character.setdefault("active_quests", [])
    result = []
    for quest_id in character["active_quests"]:
        if quest_id in quest_data_dict:
            result.append(quest_data_dict[quest_id])
    return result
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    character.setdefault("completed_quests", [])
    result = []
    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:
            result.append(quest_data_dict[quest_id])
    return result
    # TODO: Implement completed quest retrieval
    

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    character.setdefault('active_quests', [])
    character.setdefault('completed_quests', [])
    available_quests = []

    for quest_id, quest in quest_data_dict.items():
        if quest_id in character["completed_quests"]:
            continue  # Already completed
        if quest_id in character["active_quests"]:
            continue  # Already active
        req_level = quest.get("required_level", 1)
        if character.get("level", 1) < req_level:
            continue  # Level too low
        prerequisite = quest.get("prerequisite", "NONE")
        if prerequisite != "NONE" and prerequisite not in character["completed_quests"]:
            continue  # Prerequisite not met
        available_quests.append(quest)
    return available_quests
    # TODO: Implement available quest search
    # Filter all quests by requirements
    

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    character.setdefault("completed_quests", [])
    return quest_id in character["completed_quests"]
    # TODO: Implement completion check
    

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    character.setdefault("active_quests", [])
    return quest_id in character["active_quests"]
    # TODO: Implement active check
    

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    character.setdefault("active_quests", [])
    character.setdefault("completed_quests", [])

    if quest_id in character["completed_quests"]:
        return False  # Already completed
    
    if quest_id in character["active_quests"]:
        return False  # Already active
    
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        return False  # Level too low
    
    prerequisite = quest.get("prerequisite", "NONE")
    if prerequisite != "NONE" and prerequisite not in character["completed_quests"]:
        return False  # Prerequisite not met
    return True

    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found.")
    
    chain = []
    current_quest_id = quest_id
    visited = set()
    # Prevent infinite loops
    while True:
        if current_quest_id in visited:
            break 

        visited.add(current_quest_id)
        chain.append(current_quest_id)
        prerequisite = quest_data_dict[current_quest_id].get("prerequisite", "NONE")
        if not prerequisite or prerequisite == "NONE":
            break
        if prerequisite not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite quest ID '{prerequisite}' not found.")
        current_quest_id = prerequisite
    
    return chain[::-1]  # Reverse to get correct order

    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    completed = len(character.get('completed_quests', []))
    percentage = (completed / total_quests) * 100
    return float(percentage)
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0
    for quest_id in character.get("completed_quests", []):
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += int(quest.get("reward_xp", 0))
            total_gold += int(quest.get("reward_gold", 0))
    return {"total_xp": total_xp, "total_gold": total_gold}
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    result = []
    for quest in quest_data_dict.values():
        req_level = quest.get("required_level", 1)
        if min_level <= req_level <= max_level:
            result.append(quest)
    return result
    # TODO: Implement level filtering
    

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")


from flask import jsonify
from .dao.pbp_dao import PBPDao as VolleyballPBPDao
from.dao.mock.event_dao import _mockEventDAO as EventDAO


class VolleyballVolleyballPBPHandler:
    '''
    VolleyballPBPHandler - This class handles incomming requests from Odin API's gateway
                 by interacting with the PBPDAO. It is responsible for modifying
                 the state of content stored in the non-relational database,
                 especially information regarding Volleyball PBP sequences.
    @author Pedro Luis Rivera Gomez
    '''

    def __init__(self):
        """
        Default constructor - initialize keywords that apply to Volleyball PBP sequences.
        """

        self._sport_keywords = {
            "score-val": {
                "set1-opponent": 0,
                "set1-uprm": 0,
                "set2-opponent": 0,
                "set2-uprm": 0,
                "set3-opponent": 0,
                "set3-uprm": 0,
                "set4-opponent": 0,
                "set4-uprm": 0,
                "set5-opponent": 0,
                "set5-uprm": 0
            },
            "uprm-sets": ["/set1-uprm", "/set2-uprm", "/set3-uprm", "/set4-uprm", "/set5-uprm"],
            "opp-sets": ["/set1-opponent", "/set2-opponent", "/set3-opponent", "/set4-opponent", "/set5-opponent"],
            "sport": "Voleibol",
            "scoring_actions": [
                "KillPoint",
                "Ace",
                "BlockPoint",
            ],
            "personal_actions": [
                "Assist",
                "Block",
                "Dig",
            ],
            "adjust": "ScoreAdjust",
            "error_actions": [
                "AttackError",
                "ServiceError",
                "BlockingError",
                "ReceptionError"
            ],
            "notification": "Notification",
            "teams": ["uprm", "opponent"]
        }

    def _get_direct_set_path(self, team, event_id, dao):
        """
        Internal method to determine set path directly depending on the action team.
        """

        # Validate team value is specified correctly.
        if team not in self._sport_keywords["teams"]:
            raise Exception("VolleyballPBPHandler: Invalid team value.")

        current_set = int(dao.get_current_set(event_id))
        set_path = ""

        # Determine proper set path value based on the team that needs the adjust.
        if team == self._sport_keywords["teams"][0]:
            set_path = self._sport_keywords["uprm-sets"][current_set - 1]
        else:
            set_path = self._sport_keywords["opp-sets"][current_set - 1]

        return set_path

    def _get_indirect_set_path(self, team, event_id, dao):
        """
        Internal method to obtain the indirect set path. It is the complement of the direct set path.
        """

        # Validate team value is specified correctly.
        if team not in self._sport_keywords["teams"]:
            raise Exception("VolleyballPBPHandler: Invalid team value.")

        current_set = int(dao.get_current_set(event_id))
        set_path = ""

        # Determine proper set path value based on the team value (returns the opposite team set path).
        if team == self._sport_keywords["teams"][0]:
            set_path = self._sport_keywords["opp-sets"][current_set - 1]
        else:
            set_path = self._sport_keywords["uprm-sets"][current_set - 1]

        return set_path

    def _handle_pbp_action(self, event_id, action, dao):
        """
        Internal method for handling Volleyball PBP Actions via a PBPDao.
        """

        # Initial validations.
        if not dao.pbp_exists(event_id):
            raise Exception("VolleyballPBPHandler: Invalid event id.")

        if dao.is_game_over(event_id):
            raise Exception("PBPHandler: event is over.")

        action_type = action["type"]

        if not action_type:
            raise Exception("VolleyballPBPHandler: Invalid PBP action.")

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if action_type == self._sport_keywords["notification"]:
            dao.add_pbp_game_action(event_id, action)
            return

        # Adjust game actions modify the score of the direct team indicated in action["team"].
        # These are not added to the notifications feed (non-relational database).
        if action_type == self._sport_keywords["adjust"]:
            set_path = self._get_direct_set_path(action["team"], event_id, dao)
            difference = int(action["difference"])
            dao.adjust_score_by_set(event_id, set_path, difference)
            return

        is_valid_athlete = (action["athlete_id"] in dao.get_uprm_roster(event_id)
                            or action["athlete_id"] in dao.get_opponent_roster(event_id))

        # Scoring game actions modify athlete statistics and team score.
        # TODO -> TEST THIS SECTION.
        if action_type in self._sport_keywords["scoring_actions"]:

            if is_valid_athlete:
                set_path = self._get_direct_set_path(
                    action["team"], event_id, dao)
                difference = int(action["difference"])
                dao.add_pbp_game_action(event_id, action)
                dao.adjust_score_by_set(event_id, set_path, 1)
                return

            else:
                raise Exception(
                    "VolleyballPBPHandler: Invalid athlete information.")

        # Personal actions only modify athlete statistics.
        # The only action to do is add to Feed and let clients compute statistics.
        if action_type in self._sport_keywords["personal_actions"]:

            if is_valid_athlete:
                dao.add_pbp_game_action(event_id, action)
                return

            else:
                raise Exception(
                    "VolleyballPBPHandler: Invalid athlete information.")

        if action_type in self._sport_keywords["error_actions"]:

            if is_valid_athlete:
                set_path = self._get_indirect_set_path(
                    action["team"], event_id, dao)
                difference = int(action["difference"])
                dao.add_pbp_game_action(event_id, action)
                dao.adjust_score_by_set(event_id, set_path, 1)
                return

            else:
                raise Exception(
                    "VolleyballPBPHandler: Invalid athlete information.")

        raise Exception(
            "VolleyballPBPHandler: Undefined Volleyball PBP Sequence Game Action.")

    def _handle_pbp_edit_action(self, event_id, action_id, new_action, dao):
        """
        Internal method for handling editting previously added game actions in a PBP sequence.
        """

        if not dao.pbp_exists(event_id):
            raise Exception("PBPHandler: event does not exist.")

        if dao.is_game_over(event_id):
            raise Exception("PBPHandler: event is over.")

        if not dao.pbp_game_action_exists(event_id, action_id):
            raise Exception("PBPHandler: action does not exist.")

        # Every action must have a type.
        prev_action = dao.get_pbp_action(event_id, action_id)
        prev_type = prev_action["type"]
        new_type = new_action["type"]

        # Variables to be used depending on the edit type.
        are_same_type = (prev_type == new_type)
        is_valid_athlete = True

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if are_same_type and prev_type == self._sport_keywords["notification"]:
            dao.add_pbp_game_action(event_id, new_action)
            return

        # If action involves an athlete, validate the new action involves a valid athlete.
        if (new_type in self._sport_keywords["scoring_actions"]
            or new_type in self._sport_keywords["personal_actions"]
                or new_type in self._sport_keywords["error_actions"]):

            # A valid athlete must be in one of the two rosters for the given event id.
            is_valid_athlete = (new_action["athlete_id"] in dao.get_uprm_roster(event_id)
                                or new_action["athlete_id"] in dao.get_opponent_roster(event_id))

        if not is_valid_athlete:
            raise Exception("PBPHandler: Invalid athlete id.")

        if are_same_type and prev_type in self._sport_keywords["scoring_actions"]:
            new_team = new_action["team"]
            if new_team in self._sport_keywords["teams"] and new_team != prev_action["team"]:
                print("MUST REVERT SCORE IN FAVOUR OF NEW_TEAM")

            dao.edit_pbp_game_action(event_id, action_id, new_action)

        return 1

    def startPBPSequence(self, event_id):
        """
        Starts a PBP sequence.
        This function interacts with the PBP DAO to create a new PBP sequence.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_info = EventDAO().getEventById(event_id)

            if not event_info:
                return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: Invalid event."), 400

            if len(event_info) != 7:
                return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: Invalid response from Event DAO."), 500

            if event_info["sport_name"] != self._sport_keywords["sport"]:
                return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: Sport does not match Volleyball."), 403

        except:
            return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: Could not retrieve information from Event DAO."), 500

        try:
            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: PBP Sequence already created."), 403

            # At this point, the event exists and does not have a PBP sequence.
            game_metadata = {
                "game-ended": {"answer": "No"},
                "sport": event_info[4],
            }

            pbp_dao.create_volleyball_pbp_seq(
                event_id, game_metadata, self._sport_keyword["score-val"])

            return jsonify(MSG="PBP Sequence for " + id + " was successfully created"), 200

        except:
            return jsonify(ERROR="VolleyballPBPHandler.startPBPSequence: Could not retrieve information from PBP DAO."), 500

    # TODO -> TESTS & Docs...
    def setUPRMPlayer(self, event_id, player_info):
        """
        Add an athlete to UPRM roster or updates its value if exists in the system.
        This function adds an athlete to UPRM roster given it's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.setUPRMPlayer: Invalid event id."), 403

            if not player_info["number"] or not player_info["name"] or not player_info["athlete_id"]:
                return jsonify(ERROR="VolleyballPBPHandler.setUPRMPlayer: Invalid player_info. Must contain number, name, and athlete id."), 403

            pbp_dao.set_uprm_athlete(event_id, player_info)
            return jsonify(MSG="Athlete information set in the system."), 200

        except:
            return jsonify(ERROR="VolleyballPBPHandler.setUPRMPlayer: Internal error from PBP DAO."), 500

    def setOppPlayer(self, event_id,  player_info):
        """
        Add an athlete to opponent roster or updates its value if exists in the system.
        This function adds an athlete to opponent roster given it's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.setOppPlayer: Invalid event id."), 403

            if not player_info["number"] or not player_info["name"]:
                return jsonify(ERROR="VolleyballPBPHandler.setOppPlayer: Invalid player_info. Must contain number, and name."), 403

            pbp_dao.set_opponent_athlete(event_id, player_info)
            return jsonify(MSG="Athlete information set in the system."), 200

        except:
            return jsonify(ERROR="VolleyballPBPHandler.setOppPlayer: Internal error from PBP DAO."), 500

    def removeUPRMPlayer(self, event_id,  player_id):
        """
        Removes a UPRM athlete from the PBP sequence.
        This function deletes a particular UPRM athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.removeUPRMPlayer: Invalid event id."), 403

            if not player_id in pbp_dao.get_uprm_roster(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.removeUPRMPlayer: Player does not exist."), 404

            pbp_dao.remove_uprm_athlete(event_id, player_id)
            return jsonify(MSG="Athlete information removed from the system."), 200

        except:
            return jsonify(ERROR="VolleyballPBPHandler.removeUPRMPlayer: Internal error from PBP DAO."), 500

    def removeOppPlayer(self, event_id,  player_id):
        """
        Removes an opponent athlete from the PBP sequence.
        This function deletes a particular opponent athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.removeOppPlayer: Invalid event id."), 403

            if not player_id in pbp_dao.get_opponent_roster(event_id):
                return jsonify(ERROR="VolleyballPBPHandler.removeOppPlayer: Player does not exist."), 404

            pbp_dao.remove_opponent_athlete(event_id, player_id)
            return jsonify(MSG="Athlete information removed from the system."), 200

        except:
            return jsonify(ERROR="VolleyballPBPHandler.removeOppPlayer: Internal error from PBP DAO."), 500

    def addPBPAction(self, event_id, action_data):
        """
        Adds a PBP game action into the feed.
        This function interacts with the PBP DAO to insert a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.
            action_data: JSON object containing the new game action's value.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="VolleyballPBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):

                if pbp_dao.is_game_over(event_id):
                    return jsonify(ERROR="VolleyballPBPHandler.addPBPAction: PBP sequence already over."), 403
                # TODO -> validate sequence info is complete....
                self._handle_pbp_action(event_id, action_data, pbp_dao)
                return jsonify(MSG="VolleyballPBPHandler.addPBPAction: Action added into the system."), 200

            return jsonify(ERROR="VolleyballPBPHandler.addPBPAction: Non-existing PBP sequence."), 403

        except:
            return jsonify(ERROR="VolleyballPBPHandler.addPBPSequence: Could not retrieve information from PBP DAO."), 500

    # TODO -> Edit to implement a similar approach to the addPBPAction method.
    def editPBPAction(self, event_id, action_id, new_action):
        """
        Edits a PBP game action from the feed.
        This function interacts with the PBP DAO to edit a Volleyball game action
        by replacing its previous value with a new one.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to a game action id.
            new_action: JSON object containing the new game action's value.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """
        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="VolleyballPBPHandler.editPBPAction: Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):

                if pbp_dao.is_game_over(event_id):
                    return jsonify(ERROR="VolleyballPBPHandler.editPBPAction: PBP sequence already over."), 403
                self._handle_pbp_edit_action(
                    event_id, action_id, new_action, pbp_dao)
                return jsonify(MSG="Edit game action success."), 200

            return jsonify(ERROR="VolleyballPBPHandler.editPBPAction: Non-existing PBP sequence."), 403

        except:
            return jsonify(ERROR="VolleyballPBPHandler.editPBPAction: Internal error editting action."), 500

    # TODO -> Make it work same as add action (handle scoring actions...)
    def removePlayPBPAction(self, event_id, game_action_id):
        """
        Removes a PBP game action from the feed.
        This function interacts with the PBP DAO to remove a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="VolleyballPBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):

                if pbp_dao.pbp_game_action_exists(event_id, game_action_id):
                    return jsonify(pbp_dao.remove_pbp_game_action(event_id, game_action_id)), 200

                return jsonify(ERROR="VolleyballPBPHandler.setPBPSequenceOver: Non-existing game action."), 403

            return jsonify(ERROR="VolleyballPBPHandler.setPBPSequenceOver: Non-existing PBP Sequence."), 403
        except:
            return jsonify(ERROR="VolleyballPBPHandler.removePlayPBPSequence: Internal error from PBP DAO."), 500

    def setPBPSequenceOver(self, event_id):
        """
        Marks a PBP sequence state as over.
        This function interacts with the PBP DAO to modify the game-ended status of a Volleyball
        PBP sequence to true.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="VolleyballPBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            if pbp_dao.pbp_exists(event_id):
                pbp_dao.set_pbp_game_over(event_id)
                return jsonify(MSG="VolleyballPBPHandler.setPBPSequenceOver: Success."), 200

            return jsonify(ERROR="VolleyballPBPHandler.setPBPSequenceOver: Non-existing PBP Sequence."), 403

        except:
            return jsonify(ERROR="VolleyballPBPHandler.setPBPSequenceOver: Internal error from PBP DAO."), 500

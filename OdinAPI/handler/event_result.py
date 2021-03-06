from flask import jsonify
# from .dao.event import EventDAO
# from .dao.team import TeamDAO
# from .dao.athlete import AthleteDAO
from .dao.final_score_dao import FinalScoreDAO
from .dao.event_dao import EventDAO
from .dao.team_dao import TeamDAO
from .dao.athlete_dao import AthleteDAO

# THE FOLLOWING THREE ARE MOCK CLASSES FOR TESTING
# WHAT ARE WE GOING TO USE FOR TESTING? Team 1 is Basketball. Make a new event for it?
# Team 25[1,8,4], event 32, 33 are valid. event 34 is invalid. Basketball(1), 2025.
class EventResultHandler:
    # ===========================//DICTIONARY MAPPERS//==================================
    def mapEventToDict(self, record):
        pass

    # For Specific Athlete Event Info
    def mapEventAthleteStatsToDict(self, record):
        pass

    # for team statistics
    def mapEventTeamStatsToDict(self, record):
        pass

    # for final score
    def mapFinalScoreToDict(self, final_record):
        score = dict(uprm_score=final_record[0],
                     opponent_score=final_record[1])
        event_info = dict(
            event_id=final_record[2], final_score_id=final_record[3])
        return dict(event_info=event_info, score=score)

    def mapEventSeasonCollectionToDict(self, record):
        pass

    def mapEventAllStatsToDict(self, team_record, athlete_records, final_record):
        pass

# ===========================//HANDLERS//==================================
# ===========================//I.GETS//====================================

    def getAllAthleteStatisticsByEventId(self, eID, aID):
        """
        Gets all the statistics for a given event and athlete. 

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            aID: The ID of the athlete of which statistics need to be fetched

        Returns:
            A JSON containing all the statistics in the system for the specified event and athlete.
        """

        pass

    def getAllTeamStatisticsByEventId(self, eID):
        """
        Gets all the statistics for a given event. 

        Args:
            eID: The ID of the event of which team statistics need to be fetched.

        Returns:
            A JSON containing all the team statistics in the system for the specified event.
        """

        pass

    # New: get the final score only
    def getFinalScore(self, eID):
        """
        Gets the final score a given event. 

        Calls the  Final Score DAO to get event final score and maps the result to
        to a JSON that contains the final score for that event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of whichthe final score need to be fetched.

        Returns:
            A JSON containing the final score in the system for the specified event.
        """

        # validate existing event

        try:
            e_dao = EventDAO()
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error="Evento con ID:{} no se encontro.".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar evento desde el DAO."), 500

        # get final score
        try:
            dao = FinalScoreDAO()
            final_score_result = dao.getFinalScore(eID)
            if not final_score_result:
                return jsonify(Error="Puntuacion Final no se encontro para el evento con ID:{}.".format(eID)), 404
            mappedResult = self.mapFinalScoreToDict(final_score_result)
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        return jsonify(Event_Final_Score=mappedResult), 200

    def getAllAthleteStatisticsPerSeason(self, aID, seasonYear):
        """
        Gets all the statistics for a given athlete during a given season. 

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched

        Returns:
            A JSON containing all the statistics in the system for the specified athlete and season year.
        """

        pass

    # NEW
    def getAggregatedAthleteStatisticsPerSeason(self, aID, seasonYear):
        """
        Gets the aggregated statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            aID: The ID of the athlete of which statistics need to be fetched.
            seasonYear: the season year of which statistics need to be fetched.


        Returns:
            A list containing the response to the database query
            containing the aggregated statistics in the system containing 
            the matching record for the given ID and season year.
        """
        pass
    # NEW

    def getAllAggregatedAthleteStatisticsPerSeason(self, sID, seasonYear):
        """
        Gets all the aggregated statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            sID: the sport id for the basketball branch of which statistics need to be fetched
            seasonYear: the season year of which statistics need to be fetched.


        Returns:
            A list containing the response to the database query
            containing all the aggregated statistics in the system containing 
            the matching record for the season year.
        """
        pass

    # NEW
    def getAggregatedTeamStatisticsPerSeason(self, sID, seasonYear):
        """
        Gets the aggregated team statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            sID: The ID of the sport of which statistics need to be fetched.
            seasonYear: the season year of which statistics need to be fetched.


        Returns:
            A list containing the response to the database query
            containing the aggregated team statistics in the system containing 
            the matching record for the given ID and season year.
        """
        pass

    # NEW get ALL the statistics for a given event be it team or individual
    def getAllStatisticsByEventID(self, eID):
        """
        Gets all the team and individual statistics for a given event. 

        Args:
            eID: The ID of the event of which statistics need to be fetched

        Returns:
            A JSON containing all the statistics in the system for the specified event.
        """

        pass

# ===========================//II.POSTS//====================================
    # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
    def addStatistics(self, eID, aID, attributes):
        """
        Adds a new statistics record with the provided information.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.
            attributes: sports specific statistics
        Returns:
            A JSON containing the id for the new Sport Event record.
        """

        pass

    # NEW
    # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
    def addTeamStatistics(self, eID, attributes):
        """
        Adds a new team statistics record with the provided information.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            attributes:
                points: number of points scored by the athlete in the event.
                rebounds: number of rebounds attained by the athlete in the event.
                assists: number of assists attained by the athlete in the event.
                steals: number of steals attained by the athlete in the event.
                blocks: number of blocks attained by the athlete in the event.
                turnovers: number of turnovers attained by the athlete in the event.
                fieldGoalAttempt: number of field goal attempts attained by the athlete in the event.
                successfulFieldGoal: number of successful field goals attained by the athlete in the event.
                threePointAttempt: number of three point attempts attained by the athlete in the event.
                successfulThreePoint: number of successful three point shots attained by the athlete in the event.
                freeThrowAttempt: number of free throw attempts attained by the athlete in the event.
                successfulFreeThrow: number of successful free throws attained by the athlete in the event.

        Returns:
            A JSON containing the id for the new Sport Event team statistics record.
        """

        pass

    # NEW
    # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
    def addTeamStatisticsAuto(self, eID):
        """
        Adds a new team statistics record with the provided information and an aggregate of existing information.

        Args:
            eID: the ID of the event for which the statistics record will be added.

        Returns:
            A JSON containing  the id for the new Sport Event team statistics record.
        """

        pass

    # NEW
    # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
    def addFinalScore(self, eID, attributes):
        """
        Adds a new final score record with the provided information.

        Calls the FinalScoreDAO to add a final score record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the final score will be added.
            attributes:
               uprm_score: the final score of the local uprm team
               opponent_Score: the final score of the opponent


        Returns:
            A JSON containing the final score id for the new Final Score entry
        """

        # Validate Avoid Duplication

        try:
            dao = FinalScoreDAO()
            if dao.getFinalScore(eID):
                return jsonify(Error="Entrada de Puntuacion Final ya existe para Evento con ID:{}".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        # Validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error="Evento con ID:{} no se encontro.".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar evento desde el DAO."), 500

        invalid_duplicate = False
        try:
            if dao.getFinalScoreInvalid(eID):
                invalid_duplicate = True
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        # case with previously existing invalid entry, in that case update that entry
        if invalid_duplicate:
            try:
                result = dao.editFinalScore(
                    eID, attributes['uprm_score'], attributes['opponent_score'])
                if not result:
                    return jsonify(Error="Record de Puntuacion Final no se encontro para Evento con ID:{}.".format(eID)), 404
                mappedResult = self.mapFinalScoreToDict(result)
            except (TypeError, ValueError):
                return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

            dao.commitChanges()
            return jsonify(Event_Final_Score=mappedResult), 200
        else:
            # Create and Validate new Final Score entry final score
            try:
                result = dao.addFinalScore(
                    eID, attributes['uprm_score'], attributes['opponent_score'])
                if not result:
                    return jsonify(Error="Problema insertando nuevo record de Puntuacion Final."), 500
            except (TypeError, ValueError):
                return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500
            dao.commitChanges()
            return jsonify(Event_Final_Score="Se añadio nuevo record de Puntuacion Final con ID:{} para evento con ID:{}.".format(result, eID)), 201

    # NEW: the mega query
    def addAllEventStatistics(self, eID, attributes):
        """
        Adds new statistics records with the provided information.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            team_statistics: the IDs of the athletes for which the statistics record will be added.
            Attributes:
                Athlete Statistics:
                    athlete_id: the id for which the athlete statistics will be added for
                    sport-specific stats
                team_statistis: sports-specific stats
                uprm_score: the final score for the local uprm team
                opponent_score: the final score for the opponent team


        Returns:
            A JSON the id for the new Sport Event record.
        """
        pass


# ===========================//III.PUTS//====================================

    # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    def editStatistics(self, eID, aID, attributes):
        """
        Updates the statistics for the Sport event with the given IDs.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.
            attributes: sports-specific statistics

        Returns:
            A JSON containing all the user with the updated entry.
        """

        pass

    # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
    def editTeamStatistics(self, eID):
        """
        Updates the team statistics for the Sport event with the given ID and aggregates of existing data.

        Args:
            eID: the ID of the event for which the statistics record will be updated.


        Returns:
            A JSON containing all the user with the updated entry.
        """

    # NEW
    # Instantiates a sport-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
    def editFinalScore(self, eID, attributes):
        """
        Updates the final score  the basketball event with the given ID .

        Calls the FinalScoreDAO to update the final score of a basketball event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the final score record will be updated.
            attributes:
                uprm_score: the score of the local uprm team
                opponent_score: the score of the opponent team


        Returns:
            A JSON containing the final score with the updated entry.
        """
        # Validate Exists so can update

        try:
            dao = FinalScoreDAO()
            if not dao.getFinalScore(eID):
                return jsonify(Error="Entrada de Puntuacion Final de Evento no existe para Evento con ID:{}".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        # Validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error="Evento con ID:{} no se encontro.".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar evento desde el DAO."), 500

        # Update and Validate event final score, format returnable
        try:
            result = dao.editFinalScore(
                eID, attributes['uprm_score'], attributes['opponent_score'])
            if not result:
                return jsonify(Error="Record de Puntuacion Final no se encontro para Evento con ID:{}.".format(eID)), 404
            mappedResult = self.mapFinalScoreToDict(result)
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        dao.commitChanges()
        return jsonify(Event_Final_Score=mappedResult), 200

# ===========================//IV.REMOVE//====================================
    # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
    def removeStatistics(self, eID, aID):
        """
        Invalidates a statistics record in the database based on the given IDs.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            aID: the ID of the athlete for which the statistics record will be invalidated.

        Returns:
            A JSON containing the id of the invalidated record.
        """

        pass

    # NEW
    # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
    def removeTeamStatistics(self, eID):
        """
        Invalidates a team statistics record in the database based on the given ID.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.

        Returns:
            A JSON the id of the invalidated sports-specific Event.
        """

        pass

    # NEW
    # Instantiates a Final Score DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
    def removeFinalScore(self, eID):
        """
        Invalidates a final_score record in the database based on the given ID.

        Calls the FinalScoreDAO to invalidate a final score record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the final score will be invalidated.

        Returns:
            A JSON containing the final score  id of the invalidated value
        """

        # Validate existing event

        try:
            e_dao = EventDAO()
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error="Evento con ID:{} no se encontro.".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar evento desde el DAO."), 500

        # Validate Exists so can remove

        try:
            dao = FinalScoreDAO()
            if not dao.getFinalScore(eID):
                return jsonify(Error="Entrada de Puntuacion Final de Evento no existe para Evento con ID:{}".format(eID)), 400
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        # Remove Basketball_Event final score and format returnabe
        try:
            result = dao.removeFinalScore(eID)
            if not result:
                return jsonify(Error="Final Score Record not found with event id:{}.".format(eID)), 404
        except (TypeError, ValueError):
            return jsonify(Error="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(Error="No se pudo verificar Puntuacion Final desde el DAO."), 500

        dao.commitChanges()
        return jsonify(Event_Final_Score="Se removio record de Puntuacion Final con ID:{} para evento con id:{}".format(result, eID)), 200


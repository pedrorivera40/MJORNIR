import { rtdb } from '~/services/firebaseInit.js'

export default {

    // Set async function for handling Firebase set scores updates (each team has 5 set scores).
    async handleSetScores({ commit, dispatch }, event_id) {
        try {
            for (let i = 1; i <= 5; i++) {
                // Async functions for UPRM scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-uprm").on('value', function (snapshot) {
                    commit("UPDATE_UPRM_SET_SCORES", i, snapshot.val())
                });
                // Async functions for opponent scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-opponent").on('value', function (snapshot) {
                    commit("UPDATE_OPP_SET_SCORES", i, snapshot.val())
                });
            }

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve scores from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase current set updates.
    async handleCurrentSet({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/current-set").on('value', function (snapshot) {
                commit("UPDATE_CURRENT_SET", snapshot.val())
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve current set from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase UPRM roster updates.
    async handleUPRMRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_added', function (snapshot) {
                commit("ADD_UPRM_ROSTER", snapshot.key, snapshot.val());
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_changed', function (snapshot) {
                commit("UPDATE_UPRM_ROSTER", snapshot.key, snapshot.val());
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_removed', function (snapshot) {
                commit("REMOVE_UPRM_ROSTER", snapshot.key);
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving UPRM roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase opponent roster updates.
    async handleOPPRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_added', function (snapshot) {
                commit("ADD_OPP_ROSTER", snapshot.key, snapshot.val());
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_changed', function (snapshot) {
                commit("UPDATE_OPP_ROSTER", snapshot.key, snapshot.val());
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_removed', function (snapshot) {
                commit("REMOVE_OPP_ROSTER", snapshot.key);
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving opponent roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase game-over updates.
    async handleGameOver({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/game-over").on('value', function (snapshot) {
                commit("SET_GAME_OVER", snapshot.val())
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve game over from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase opponent color updates.
    async handleOppColor({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/opp-color").on('value', function (snapshot) {
                commit("SET_OPP_COLOR", snapshot.val())
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve opponent color from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase game action updates.
    async handleGameActions({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_added', function (snapshot) {
                commit("ADD_GAME_ACTION", snapshot.key, snapshot.val());
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_changed', function (snapshot) {
                commit("UPDATE_GAME_ACTION", snapshot.key, snapshot.val())
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_removed', function (snapshot) {
                commit("REMOVE_GAME_ACTION", snapshot.key)
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving game actions update from RTDB.", color: "error" }, { root: true });
        }
    },
}
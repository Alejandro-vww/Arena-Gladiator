import time

from game_dict import GameDict
from aplication_status import AplicationStatus


class MessageProcessor:

    def __init__(self):
        self.game_dict = GameDict()
        self.app_status = AplicationStatus()

    def update(self, transaction):
        # Changes in client screen
        if screen_val := transaction.get('toSceneName'):
            self.app_status.screen = screen_val
        # Entering o exiting game room
        if match_val := transaction.get('matchGameRoomStateChangedEvent'):
            self.process_matchGameRoomStateChangedEvent(match_val)
        # To user messages
        if gre_2_client := transaction.get('greToClientEvent', {}).get('greToClientMessages'):
            list(map(self.process_messages, gre_2_client))
        # Actions and cursor
        if client_2_match_type := transaction.get('clientToMatchServiceMessageType'):
            # Actions
            if client_2_match_type == 'ClientToMatchServiceMessageType_ClientToGREMessage':
                self.game_dict.client_2_match = transaction
                self.process_actions()
            # Cursor
            if client_2_match_type == 'ClientToMatchServiceMessageType_ClientToGREUIMessage':
                self.game_dict.UI_state = transaction
        if username := transaction.get('authenticateResponse', {}).get('screenName'):
            self.game_dict.username = username

        self.game_dict.last_actualization = time.time()
        pass

    def process_matchGameRoomStateChangedEvent(self, match_val):
        self.game_dict.game_room_info.update(match_val)
        game_info = match_val.get('gameRoomInfo', {}).get('stateType')
        if game_info == 'MatchGameRoomStateType_Playing':
            self.app_status.screen ='Playing'
            self.app_status.win = None
            self.app_status.mulligan = True
        else:
            self.app_status.screen = 'GameEnded'
            self.app_status.mulligan = False
            self.reset_all_dictionary()
            try:
                winning_team = match_val['gameRoomInfo']['finalMatchResult']['resultList'][0]['winningTeamId']
                winner = match_val['gameRoomInfo']['gameRoomConfig']['reservedPlayers'][winning_team-1]['playerName']
                result = winner == self.game_dict.username
                self.app_status.win = result
            except KeyError:
                self.app_status.win = None


    def process_messages(self, message):
        if message.get('type') == 'GREMessageType_GameStateMessage':
            game_state = message.get('gameStateMessage')
            if game_state.get('type') == 'GameStateType_Diff':
                for key, value in game_state.items():
                    if key == 'gameObjects':
                        self.update_game_objects(game_state['gameObjects'])
                    elif key == 'zones':
                        self.update_zones(game_state['zones'])
                    elif key == 'players':
                        self.update_players(game_state['players'])
                    else:
                        self.game_dict.game_state[key] = game_state[key]
            elif game_state.get('type') == 'GameStateType_Full':
                self.game_dict.game_state = game_state
        else:
            self.game_dict.other_dicts[message.get('type')] = message

    def process_actions(self):
        action = self.game_dict.client_2_match
        if action.get('payload', {}).get('type') == 'ClientMessageType_MulliganResp':
            mulligan_resp = action.get('payload', {}).get('mulliganResp', {}).get('decision')
            self.app_status.mulligan = mulligan_resp == 'MulliganOption_Mulligan'
        else:
            pass

    def update_game_objects(self, game_obj_diff):
        game_objects = self.game_dict.game_objects
        old_ids = list(inst['instanceId'] for inst in game_objects)
        for new_instance in game_obj_diff:
            if new_instance['instanceId'] in old_ids:
                index = old_ids.index(new_instance['instanceId'])
                game_objects[index] = new_instance
            else:
                game_objects.append(new_instance)
        self.game_dict.game_state['gameObjects'] = game_objects

    def update_zones(self, zones_diff):
        zones = self.game_dict.game_state.get('zones')
        old_ids = list(zone['zoneId'] for zone in zones)
        for new_zone in zones_diff:
            if new_zone['zoneId'] in old_ids:
                index = old_ids.index(new_zone['zoneId'])
                zones[index] = new_zone
            else:
                zones.append(new_zone)
        self.game_dict.game_state['zones'] = zones

    def update_players(self, players_diff):
        players = self.game_dict.game_state.get('players')
        for new_player in players_diff:
            for player_dict in players:
                if player_dict.get('teamId') == new_player.get('teamId'):
                    player_dict.update(new_player)
        self.game_dict.game_state['players'] = players

    def reset_all_dictionary(self):
        self.game_dict.game_state = {}
        self.game_dict.game_room_info = {}
        self.game_dict.instances.reset()
        self.game_dict.other_dicts = {}
        self.game_dict.UI_state = {}
        self.game_dict.client_2_match = {}

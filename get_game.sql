DELIMITER //
CREATE PROCEDURE get_game(IN game_name VARCHAR(255), IN slack_team_id VARCHAR(255))
   BEGIN
   	  DECLARE team_id INT;
   	  SET team_id = (SELECT ID FROM Teams WHERE SlackTeamID = slack_team_id);
      SELECT ID FROM Games WHERE Name = game_name AND TeamID = team_id;
   END//
DELIMITER ;
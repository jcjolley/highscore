DELIMITER //
CREATE PROCEDURE get_or_create_game(IN game_name VARCHAR(255), IN slack_team_id VARCHAR(255))
   BEGIN
   	  DECLARE team_id INT;
   	  SET team_id = (SELECT ID FROM Teams WHERE SlackTeamID = slack_team_id);

      IF EXISTS (SELECT * FROM Games WHERE Name = game_name AND TeamID = team_id) THEN
         SELECT ID FROM Games WHERE Name = game_name AND TeamID = team_id;
      ELSE
         INSERT INTO Games (TeamID, Name) VALUES (team_id, game_name);
         SELECT LAST_INSERT_ID() as "ID";
      END IF;
   END//
DELIMITER ;
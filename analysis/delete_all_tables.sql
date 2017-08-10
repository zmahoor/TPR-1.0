SET SQL_SAFE_UPDATES = 0;

delete from TwitchPlays.users;
delete from TwitchPlays.robots;
delete from TwitchPlays.helps;
delete from TwitchPlays.chats;
delete from TwitchPlays.unique_commands;

delete from TwitchPlays.display;
delete from TwitchPlays.command_log;
delete from TwitchPlays.reward_log;

ALTER TABLE TwitchPlays.chats AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.users AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.robots AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.helps AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.unique_commands AUTO_INCREMENT = 1;

ALTER TABLE TwitchPlays.command_log AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.reward_log AUTO_INCREMENT = 1;
ALTER TABLE TwitchPlays.display AUTO_INCREMENT = 1;


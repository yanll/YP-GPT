

ALTER TABLE  gpts_conversations
    ADD COLUMN `ext_status` varchar(64) not null default 'ENABLED' comment '扩展状态：ENABLED/DISABLED';

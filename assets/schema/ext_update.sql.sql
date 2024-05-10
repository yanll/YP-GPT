ALTER TABLE gpts_conversations
    ADD COLUMN `ext_status` varchar(64) not null default 'ENABLED' comment '扩展状态：ENABLED/DISABLED';



drop table app_chat_history_message;
create table app_chat_history_message
(
    id              varchar(64) primary key comment '主键',
    agent_name      varchar(128) not null default '' comment '代理名称',
    node_name       varchar(128) not null default '' comment '节点名称',
    conv_uid        varchar(64)  not null default '' comment '会话用户',
    `index`         int(10) not null default '0' comment '顺序',
    `round_index`   int(10) not null default '0' comment '轮次',
    message_type    varchar(128) not null default '' comment '消息类型：human/assistant/ai/system/user',
    display_type    varchar(128) not null default '' comment '展示类型',
    lark_message_id varchar(128) not null default '' comment '飞书消息主键',
    content         text null comment '消息内容',
    message_detail  text null comment '消息详情',
    comment_type    varchar(128) not null default '' comment 'like/unlike',
    status          varchar(32)  not null default 'ENABLED' comment 'ENABLED、DISABLED、DELETED',
    created_time    datetime null default current_timestamp comment '创建时间',
    modified_time   datetime null default current_timestamp on update current_timestamp comment '更新时间'
) comment '应用会话历史';

ALTER TABLE app_chat_history_message
    ADD COLUMN display_type varchar(128) not null default '' comment '展示类型：',
    ADD COLUMN lark_message_id varchar(128) not null default '' comment '飞书消息主键',
    ADD COLUMN comment_type         varchar(128) not null default '' comment_type 'like/unlike';



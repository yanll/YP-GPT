export type IEditorSQLRound = {
  db_name: string;
  round: number;
  round_name: string;
};

export type GetEditorSQLRoundRequest = IEditorSQLRound[];

export type PostEditorSQLRunParams = {
  db_name: string;
  sql: string;
};

export type PostEditorChartRunParams = {
  db_name: string;
  sql?: string;
  chart_type?: string;
};

export type PostEditorChartRunResponse = {
  sql_data: {
    result_info: string;
    run_cost: string;
    colunms: string[];
    values: Record<string, any>[];
  };
  chart_values: Record<string, any>[];
  chart_type: string;
};

export type PostSQLEditorSubmitParams = {
  conv_uid: string;
  db_name: string;
  conv_round?: string | number | null;
  old_sql?: string;
  old_speak?: string;
  new_sql?: string;
  new_speak?: string;
};

export type PostEditorSqlParams = {
  con_uid: string;
  round: string | number;
};

export type PostEditorSqlRequest = {};

export type GetEditorySqlParams = { con_uid: string; round: string | number };


export interface EditorValueProps {
  sql?: string;
  thoughts?: string;
  title?: string;
  showcase?: string;
}

export interface RoundProps {
  db_name: string;
  round: number;
  round_name: string;
}



export interface ITableTreeItem {
  title: string;
  key: string;
  type: string;
  default_value: string | null;
  can_null: string;
  comment: string | null;
  children: Array<ITableTreeItem>;
}
import { ChatContext } from '@/app/chat-context';
import { apiInterceptors, postChatModeParamsList } from '@/client/api';
import { IDB } from '@/types/chat';
import { dbMapper } from '@/utils';
import { useAsyncEffect } from 'ahooks';
import { Select } from 'antd';
import { useContext, useEffect, useMemo, useState } from 'react';
import DBIcon from '@/components/common/db-icon';

function DBSelector() {
  const { scene, dbParam, setDbParam, tableParam, setTableParam } = useContext(ChatContext);

  const [dbs, setDbs] = useState<IDB[]>([]);

  useAsyncEffect(async () => {
    const [, res] = await apiInterceptors(postChatModeParamsList(scene as string));
    setDbs(res ?? []);
  }, [scene]);

  const dbOpts = useMemo(
    () =>
      dbs.map?.((db: IDB) => {
        return { name: db.param, ...dbMapper[db.type] };
      }),
    [dbs],
  );

  useEffect(() => {
    if (dbOpts?.length && !dbParam) {
      setDbParam(dbOpts[0].name);
    }
  }, [dbOpts, setDbParam, dbParam]);

  if (!dbOpts?.length) return null;

  return (
    <>
      <Select
        value={dbParam}
        className="w-56"
        onChange={(val) => {
          setDbParam(val);
        }}
      >
        {dbOpts.map((item) => (
          <Select.Option key={item.name}>
            <DBIcon width={24} height={24} src={item.icon} label={item.label} className="w-[1.5em] h-[1.5em] mr-1 inline-block mt-[-4px]" />
            {item.name}
          </Select.Option>
        ))}
      </Select>
      {/* {process.env.NODE_ENV} */}
      <Select
        value={tableParam}
        className="w-56"
        onChange={(val) => {
          setTableParam(val);
        }}
      >
        {process.env.NODE_ENV === "development" && <Select.Option key={'my_first_table'}>
          my_first_table
        </Select.Option>}
        {process.env.NODE_ENV === "development" && <Select.Option key={'my_second_table'}>
          my_second_table
        </Select.Option>}


        {process.env.NODE_ENV !== "development" && <Select.Option key={'dp_dws_dw_event_trx_pay'}>
          dp_dws_dw_event_trx_pay
        </Select.Option>}
        {process.env.NODE_ENV !== "development" && <Select.Option key={'DM_BI_DAILYTRXSTAT_PANEL_PAYER_VIEW_HC_DBVIEW'}>
          DM_BI_DAILYTRXSTAT_PANEL_PAYER_VIEW_HC_DBVIEW
        </Select.Option>}
      </Select>

    </>
  );
}

export default DBSelector;

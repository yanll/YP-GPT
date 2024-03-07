import React from 'react';
import { Table } from '@mui/joy';

import { Empty } from 'antd';
import MonacoEditor from '../monaco-editor';

import { OnChange } from '@monaco-editor/react';
import Chart from '../../chart';
import { EditorValueProps } from '@/types/editor';


interface IProps {
  editorValue?: EditorValueProps;
  chartData?: any;
  tableData?: any;
  handleChange: OnChange;
}

function DbEditorContent({ editorValue, chartData, tableData, handleChange }: IProps) {
  const chartWrapper = React.useMemo(() => {
    if (!chartData) return <div></div>;
    return (
      <div className="flex-1 overflow-auto p-3" style={{ flexShrink: 0, overflow: 'hidden' }}>
        <Chart chartsData={[chartData]} />
      </div>
    );
  }, [chartData]);

  return (
    <>
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1" style={{ flexShrink: 0, overflow: 'auto' }}>
          <MonacoEditor value={editorValue?.sql || ''} language="mysql" onChange={handleChange} thoughts={editorValue?.thoughts || ''} />
        </div>
        {chartWrapper}
      </div>
      <div className="h-96 border-[var(--joy-palette-divider)] border-t border-solid overflow-auto">
        {tableData?.values?.length > 0 ? (
          <Table aria-label="basic table" stickyHeader>
            <thead>
              <tr>
                {tableData?.columns?.map((column: any, i: number) => (
                  <th key={column + i}>{column}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData?.values?.map((value: any, i: number) => (
                <tr key={i}>
                  {Object.keys(value)?.map((v) => (
                    <td key={v}>{value[v]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        ) : (
          <div className="h-full flex justify-center items-center">
            <Empty />
          </div>
        )}
      </div>
    </>
  );
}

export default DbEditorContent;

import 'handsontable/dist/handsontable.full.min.css';
import { HotTable } from '@handsontable/react';

function Mess() {
    return(
        <HotTable
            data={[
                ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday', 'Sunday'],
                ['2019', 10, 11, 12, 13],
                ['2020', 20, 11, 14, 13],
                ['2021', 30, 15, 12, 13]
            ]}
            rowHeaders={true}
            colHeaders={true}
            height="auto"
            licenseKey="non-commercial-and-evaluation" // for non-commercial use only
        />
    );
}
export default Mess;
import { NotebookPanel } from '@jupyterlab/notebook';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { createSelectAuthTypeWidget } from '../SelectAuthypeWidget';
import { ClusterState, ClusterRowType } from '../constants/types';

const mockCluster: ClusterRowType = {
  name: 'Cluster-3',
  id: '3333',
  status: {
    state: ClusterState.Running,
  },
};

jest.mock('../utils/SelectAuthUtil', () => ({ handleConnect: jest.fn() }));

let notebookPanel: NotebookPanel;
let app: JupyterFrontEnd;
const eventDetail = 'eventName';
const disposeDialog = jest.fn();

describe('SelectAuthTypeWidget', () => {
  it('should render SelectAuthType component with selected cluster', () => {
    const widget = createSelectAuthTypeWidget(disposeDialog, mockCluster, app, eventDetail, notebookPanel);
    const element = widget.render();
    expect(element.props.selectedCluster).toEqual(mockCluster);
  });
});

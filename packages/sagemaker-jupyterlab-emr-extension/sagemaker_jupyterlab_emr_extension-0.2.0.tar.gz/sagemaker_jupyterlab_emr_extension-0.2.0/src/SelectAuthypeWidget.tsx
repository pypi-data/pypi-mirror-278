/* eslint-disable no-console */
import React from 'react';
import { Dialog } from '@jupyterlab/apputils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { SelectAuthType } from './components/SelectAuthType';
import { ClusterRowType, ShowNotificationHandlerType } from './constants/types';

// @ts-ignore
class SelectAuthTypeWidget implements Dialog.IBodyWidget {
  readonly disposeDialog: ShowNotificationHandlerType;
  readonly selectedCluster: ClusterRowType;
  readonly app: JupyterFrontEnd;
  readonly eventDetail: string;
  readonly notebookPanel: NotebookPanel | undefined;

  constructor(
    disposeDialog: ShowNotificationHandlerType,
    selectedCluster: ClusterRowType,
    app: JupyterFrontEnd,
    eventDetail: string,
    notebookPanel?: NotebookPanel,
  ) {
    this.disposeDialog = disposeDialog;
    this.selectedCluster = selectedCluster;
    this.app = app;
    this.eventDetail = eventDetail;
    this.notebookPanel = notebookPanel;
  }

  render() {
    return (
      <SelectAuthType
        onCloseModal={this.disposeDialog}
        selectedCluster={this.selectedCluster}
        app={this.app}
        eventDetail={this.eventDetail}
        notebookPanel={this.notebookPanel}
      />
    );
  }
}

const createSelectAuthTypeWidget = (
  disposeDialog: () => void,
  selectedCluster: ClusterRowType,
  app: JupyterFrontEnd,
  eventDetail: string,
  notebookPanel?: NotebookPanel,
) => new SelectAuthTypeWidget(disposeDialog, selectedCluster, app, eventDetail, notebookPanel);

export { createSelectAuthTypeWidget };

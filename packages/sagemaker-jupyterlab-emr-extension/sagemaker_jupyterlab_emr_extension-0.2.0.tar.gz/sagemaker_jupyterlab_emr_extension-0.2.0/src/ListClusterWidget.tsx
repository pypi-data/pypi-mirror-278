import React, { Suspense } from 'react';
import { Dialog } from '@jupyterlab/apputils';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ListClusterView } from './components/ListClusterView';
import { ShowNotificationHandlerType } from './constants/types';

// @ts-ignore
class ListClusterWidget implements Dialog.IBodyWidget {
  readonly disposeDialog: any;
  readonly header: JSX.Element;
  readonly app: JupyterFrontEnd;
  readonly eventDetail: string;

  constructor(
    disposeDialog: ShowNotificationHandlerType,
    header: JSX.Element,
    app: JupyterFrontEnd,
    eventDetail: string,
  ) {
    this.disposeDialog = disposeDialog;
    this.header = header;
    this.app = app;
    this.eventDetail = eventDetail;
  }

  render() {
    return (
      <Suspense fallback={null}>
        <ListClusterView
          onCloseModal={this.disposeDialog}
          header={this.header}
          app={this.app}
          eventDetail={this.eventDetail}
          data-testid="list-cluster-view"
        />
      </Suspense>
    );
  }
}

const createListClusterWidget = (
  disposeDialog: () => void,
  header: JSX.Element,
  app: JupyterFrontEnd,
  eventDetail: string,
) => new ListClusterWidget(disposeDialog, header, app, eventDetail);

export { createListClusterWidget };

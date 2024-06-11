import { Dialog, ISessionContext } from '@jupyterlab/apputils';
import { AuthType, ClusterRowType, i18nStrings } from '../constants';
import { ModalHeader } from '../components/Modal/ModalHeader';
import React from 'react';
import { createSelectAuthTypeWidget } from '../SelectAuthypeWidget';
import { cx } from '@emotion/css';
import styles from '../components/Modal/styles';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { COMMANDS } from './CommandUtils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { getAuthTypeFromCluster } from './AuthTypeUtil';

export const openSelectAuthType = async (
  selectedCluster: ClusterRowType,
  app: JupyterFrontEnd,
  eventDetail: string,
) => {
  let dialog: any = {};
  const disposeDialog = () => dialog && dialog.resolve();
  dialog = new Dialog({
    title: (
      <ModalHeader
        heading={`${i18nStrings.Clusters.selectAuthTitle}"${selectedCluster.name}"`}
        shouldDisplayCloseButton={true}
        onClickCloseButton={disposeDialog}
      />
    ),
    body: createSelectAuthTypeWidget(disposeDialog, selectedCluster, app, eventDetail, undefined).render(),
  });

  dialog.addClass(cx(styles.ModalBase, styles.Footer, styles.DialogClassname));
  dialog.launch();
};

export const handleConnect = (
  disposeDialog: () => void,
  selectedCluster: ClusterRowType | undefined,
  app: JupyterFrontEnd,
  eventDetail: string,
  type?: AuthType,
  sessionContext?: ISessionContext,
  notebookPanel?: NotebookPanel,
) => {
  /*
   * Cluster id is based on customer selection
   * Auth type is based on the customer's cluster properties
   * Auth options: Kerberos, None, Basic_Access
   * Language options: scala, python
   */
  return () => {
    if (!selectedCluster || !app) return;

    const authType = type || getAuthTypeFromCluster(selectedCluster);

    if (!authType) {
      // close previous dialog and open a new one for selecting auth type
      disposeDialog();
      openSelectAuthType(selectedCluster, app, eventDetail);
    } else {
      disposeDialog();
      app.commands.execute(COMMANDS.emrConnect.id, {
        clusterId: selectedCluster.id,
        authType: authType,
        language: 'python', // This option is hardcoded by default
      });
    }

    if (window && window.panorama) {
      window.panorama('trackCustomEvent', {
        eventType: 'eventDetail',
        eventDetail: eventDetail,
        eventContext: 'JupyterLab',
        timestamp: Date.now(),
      });
    }
  };
};

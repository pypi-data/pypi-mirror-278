import { IRouter, JupyterFrontEnd } from '@jupyterlab/application';
import { URLExt } from '@jupyterlab/coreutils';
import { showErrorMessage } from '@jupyterlab/apputils';
import { i18nStrings } from '../constants/i18n';
import { describeCluster } from '../service/presignedURL';
import { openSelectAuthType } from '../utils/SelectAuthUtil';
import { ClusterRowType } from '../constants';
import { getAuthTypeFromCluster } from '../utils/AuthTypeUtil';
import { COMMANDS } from '../utils/CommandUtils';
import { sleep } from '../utils/CommonUtils';

const il18stringsError = i18nStrings.EmrClustersDeeplinking.errorDialog;

// IRouter pattern could be matched arbitrary number of times.
// This flag is to ensure the plugin is triggered only once during re-direction.
let isPatternMatched = false;

/**
 * Function to attach EMR cluster to a new notebook
 * @param router
 * @param app
 * @returns
 */
const executeAttachClusterToNewNb = async (router: IRouter, app: JupyterFrontEnd) => {
  const eventDetail = 'EMR-Attach-To-New-Notebook';
  if (isPatternMatched) {
    return;
  }
  try {
    const { search } = router.current;
    if (!search) {
      await showErrorMessageAsync(il18stringsError.invalidRequestErrorMessage);
      return;
    }

    app.restored.then(async () => {
      const { clusterId } = URLExt.queryStringToObject(search);
      if (!clusterId) {
        await showErrorMessageAsync(il18stringsError.invalidRequestErrorMessage);
        return;
      }

      const clusterDetails = await describeCluster(clusterId);
      if (!clusterDetails || !clusterDetails?.cluster) {
        await showErrorMessageAsync(il18stringsError.invalidClusterErrorMessage);
        return;
      }

      // Execute create new notebook command
      const notebookPanel = await app.commands.execute('notebook:create-new');
      await new Promise((resolve) => {
        notebookPanel.sessionContext.kernelChanged.connect((context: any, kernel: unknown) => {
          resolve(kernel);
        });
      });

      const clusterRow: ClusterRowType = {
        name: clusterDetails.cluster.name,
        id: clusterDetails.cluster.id,
        status: {
          state: clusterDetails.cluster.status,
        },
        configurations: clusterDetails.cluster.configurations,
        kerberosAttributes: clusterDetails.cluster.kerberosAttributes,
      };

      // Open Auth Selection pop up
      const authType = getAuthTypeFromCluster(clusterRow);
      if (authType) {
        await sleep(2000); // Sleep for 2 sec for the kernel to start up.
        await app.commands.execute(COMMANDS.emrConnect.id, {
          clusterId: clusterRow.id,
          authType: authType,
          language: 'python', // This option is hardcoded by default
        });
      } else {
        await openSelectAuthType(clusterRow, app, eventDetail);
      }
    });
  } catch (error) {
    await showErrorMessageAsync(il18stringsError.defaultErrorMessage);
    return;
  } finally {
    isPatternMatched = true;
  }
};

const showErrorMessageAsync = async (message: string) => {
  return showErrorMessage(il18stringsError.errorTitle, {
    message: message,
  });
};

export { executeAttachClusterToNewNb };

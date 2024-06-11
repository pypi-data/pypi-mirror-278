import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { cx } from '@emotion/css';
import { CircularProgress } from '@mui/material';
import { Footer } from './Footer';
import { GetColumnConfig } from './GetColumnConfig';
import { EmrExpandedClustersTable, TableConfig } from './EmrExpandableClustersTable/EmrExpandableClustersTable';
import { arrayHasLength } from '../utils/CommonUtils';
import { i18nStrings } from '../constants/i18n';
import { ModalBodyContainer, GridWrapper } from './EmrExpandableClustersTable/styles';
import { Cluster, ClusterRowType, HandleConnectType } from '../constants/types';
import { DESCRIBE_CLUSTER_URL, LIST_CLUSTERS_URL } from '../service/constants';
import { fetchApiResponse, OPTIONS_TYPE } from '../service/fetchApiWrapper';
import { Arn } from '../utils/ArnUtils';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { handleConnect } from '../utils/SelectAuthUtil';

interface ListClusterProps extends React.HTMLAttributes<HTMLElement> {
  readonly onCloseModal: () => void;
  readonly header: JSX.Element;
  readonly app: JupyterFrontEnd;
  readonly eventDetail: string;
}

const DEFAULT_TABLE_CONFIG: TableConfig = {
  width: 850,
  height: 500,
};

const ListClusterView: React.FC<ListClusterProps> = (ListClusterProps) => {
  const { onCloseModal, header, app, eventDetail } = ListClusterProps;
  const getConnectHandler: HandleConnectType = handleConnect;

  const [clustersData, setClustersData] = useState<any>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState<any>('');
  const [clusterDetails, setClusterDetails] = useState<Cluster | undefined>(undefined);
  const [selectedId, setSelectedId] = useState<string | undefined>();
  const [, setSelectedAccountId] = useState<string>(''); // Need accountId later for phase2
  const [isConnectButtonDisabled, setIsConnectButtonDisabled] = useState<boolean>(true);
  const columnConfig = GetColumnConfig();

  const getListClusterData = async (marker = '') => {
    try {
      setIsLoading(true);
      const params = JSON.stringify({
        ClusterStates: ['RUNNING', 'WAITING'],
        ...(marker && { Marker: marker }),
      });

      const data = await fetchApiResponse(LIST_CLUSTERS_URL, OPTIONS_TYPE.POST, params);
      if (data && data.clusters) {
        setClustersData((prevData: any) => [...prevData, ...data.clusters]);
        if (data && data.Marker) {
          getListClusterData(data.Marker);
        } else {
          setIsLoading(false);
        }
      }

      if (!arrayHasLength(data)) {
        setIsLoading(false);
        setIsError(data.message);
      }
    } catch (error: any) {
      setIsLoading(false);
      setIsError(error.message);
    }
  };

  useEffect(() => {
    getListClusterData();
  }, []);

  const getClusterDetails = async (selectedId: string) => {
    const params = JSON.stringify({
      ClusterId: selectedId,
    });

    const data = await fetchApiResponse(DESCRIBE_CLUSTER_URL, OPTIONS_TYPE.POST, params);
    setClusterDetails(data.cluster);
  };

  useEffect(() => {
    if (selectedId) {
      setClusterDetails(getClusterDetails(selectedId) as any);
    }
  }, [selectedId]);

  //sort the listCluster data by Name
  const clustersList = useMemo(
    () =>
      clustersData?.sort((a: ClusterRowType, b: ClusterRowType) => {
        const clusterA = a.name as string;
        const clusterB = b.name as string;
        return clusterA?.localeCompare(clusterB);
      }),
    [clustersData],
  );

  const getSelectedClusterAccountId = useCallback(
    (selectedClusterId: string) => {
      const selectedCluster = clustersList.find(
        (cluster: { id: string }) => cluster.id === selectedClusterId,
      ) as unknown as Cluster;
      let accountId = '';
      const clusterArn = selectedCluster?.clusterArn;

      if (clusterArn && Arn.isValid(clusterArn)) accountId = Arn.fromArnString(clusterArn).accountId;
      return accountId;
    },
    [clustersList],
  );

  const getSelectedClusterArn = useCallback(
    (selectedClusterId: string) => {
      const cluster: any = clustersList.find((cluster: { id: string }) => cluster.id === selectedClusterId);
      const clusterArn = cluster?.clusterArn;
      if (clusterArn && Arn.isValid(clusterArn)) return clusterArn;
      return '';
    },
    [clustersList],
  );

  const handleRowSelection = useCallback(
    (selectedRow: ClusterRowType): void => {
      const selectedRowId = selectedRow?.id;

      if (selectedRowId && selectedRowId === selectedId) {
        setSelectedId(selectedRowId);
        setSelectedAccountId('');
        setIsConnectButtonDisabled(true);
      } else {
        setSelectedId(selectedRowId);
        setSelectedAccountId(getSelectedClusterAccountId(selectedRowId));
        setIsConnectButtonDisabled(false);

        if (window && window.panorama) {
          window.panorama('trackCustomEvent', {
            eventType: 'eventDetail',
            eventDetail: 'EMR-Modal-ClusterRow',
            eventContext: 'JupyterLab',
            timestamp: Date.now(),
          });
        }
      }
    },
    [selectedId, getSelectedClusterAccountId],
  );

  const ListDataGrid = () => {
    return (
      <>
        <div className={cx(GridWrapper, 'grid-wrapper')}>
          <EmrExpandedClustersTable
            clustersList={clustersList}
            selectedClusterId={selectedId ?? ''}
            clusterArn={getSelectedClusterArn(selectedId ?? '')}
            accountId={getSelectedClusterAccountId(selectedId ?? '')}
            tableConfig={DEFAULT_TABLE_CONFIG}
            clusterManagementListConfig={columnConfig}
            onRowSelect={handleRowSelection}
            clusterDetails={clusterDetails}
          />
        </div>
      </>
    );
  };

  const onConnect = () => {
    getConnectHandler(onCloseModal, clusterDetails as any, app, eventDetail, undefined, undefined, undefined)();
  };

  const getErrorMessage = (errorMessage: string) => {
    const documentationLink = (
      <a href="https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-configure-discoverability-emr-cluster.html">
        documentation
      </a>
    );

    if (errorMessage.includes('permission error')) {
      return (
        <span className="error-msg">
          {i18nStrings.Clusters.permissionError} {documentationLink}
        </span>
      );
    } else {
      return <span className="error-msg">{errorMessage}</span>;
    }
  };

  return (
    <>
      {isError && <span className="no-cluster-msg">{getErrorMessage(isError)}</span>}
      {isLoading ? (
        <span>
          <CircularProgress size="1rem" />
        </span>
      ) : arrayHasLength(clustersData) ? (
        <div className={cx(ModalBodyContainer, 'modal-body-container')}>
          {header}
          {ListDataGrid()}
        </div>
      ) : (
        <div className="no-cluster-msg">{i18nStrings.Clusters.noCluster}</div>
      )}
      <Footer onCloseModal={onCloseModal} onConnect={onConnect} disabled={isConnectButtonDisabled} />
    </>
  );
};

export { ListClusterProps, ListClusterView };

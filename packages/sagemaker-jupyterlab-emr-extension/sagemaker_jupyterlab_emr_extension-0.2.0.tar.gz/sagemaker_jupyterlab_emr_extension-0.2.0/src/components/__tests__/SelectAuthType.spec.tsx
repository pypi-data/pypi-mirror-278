import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { SelectAuthType } from '../SelectAuthType';
import { i18nStrings } from '../../constants/i18n';
import { JupyterFrontEnd } from '@jupyterlab/application';

// Mock the necessary props and functions
const eventDetailMock = 'eventDetailMock';
const app = null as unknown as JupyterFrontEnd;

jest.mock('../../utils/SelectAuthUtil', () => ({ handleConnect: jest.fn() }));

const mockProps = {
  onCloseModal: jest.fn(),
  selectedCluster: undefined,
  app: app,
  eventDetail: eventDetailMock,
  notebookPanel: undefined,
};

describe('SelectAuthType', () => {
  it('renders component with default auth type', () => {
    const { getByLabelText } = render(<SelectAuthType {...mockProps} />);

    // Ensure that the component renders with default auth type 'Basic_Access'
    expect(getByLabelText(i18nStrings.Clusters.radioButtonLabels.basicAccess)).toBeInTheDocument();
    expect(getByLabelText(i18nStrings.Clusters.radioButtonLabels.noCredential)).toBeInTheDocument();
  });

  it('renders the component with default auth type', () => {
    const { getByLabelText } = render(
      <SelectAuthType
        onCloseModal={() => {}}
        selectedCluster={undefined}
        app={app}
        eventDetail="eventDetailMock"
        notebookPanel={undefined}
      />,
    );

    const basicAccessRadio = getByLabelText(i18nStrings.Clusters.radioButtonLabels.basicAccess);
    const noCredentialRadio = getByLabelText(i18nStrings.Clusters.radioButtonLabels.noCredential);

    expect(basicAccessRadio).toBeChecked();
    expect(noCredentialRadio).not.toBeChecked();
  });
});

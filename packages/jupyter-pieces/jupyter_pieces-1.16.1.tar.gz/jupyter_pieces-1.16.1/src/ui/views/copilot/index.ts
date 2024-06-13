import {
  AnchorTypeEnum,
  CapabilitiesEnum,
  SeedTypeEnum,
} from '@pieces.app/pieces-os-client';
import { defaultApp, pluginSettings } from '../../..';
import { loadConnect } from '../../../connection/api_wrapper';
import ConnectorSingleton from '../../../connection/connector_singleton';
import ShareableLinksService from '../../../connection/shareable_link';
import copyToClipboard from '../../utils/copyToClipboard';
import langExtToClassificationSpecificEnum from '../../utils/langExtToClassificationSpecificEnum';
import { CopilotState } from 'copilot/dist/types/ConversationState';
import { CopilotParams } from 'copilot/dist/types/CopilotParams';
import QGPTView from 'copilot/dist/view/QGPTView';
import AddSnippetToContextModal from '../../modals/AddSnippetToContextModal';
import PiecesDatabase from '../../../database/PiecesDatabase';
import Notifications from '../../../connection/notification_handler';
import { CopilotAnalytics } from 'copilot/dist/types/CopilotAnalytics.enum';
import { SegmentAnalytics } from '../../../analytics/SegmentAnalytics';
import { TerminalManager } from '@jupyterlab/services';
import {
  NotificationActionTypeEnum,
  NotificationAction,
} from 'copilot/dist/types/NotificationParameters';
import { setStored } from '../../../localStorageManager';

const getApplication = async () => {
  if (!ConnectorSingleton.getInstance().context) await loadConnect();
  return ConnectorSingleton.getInstance().context.application;
};

export let copilotState: CopilotState = {
  conversation: [],
  conversationId: '',
  selectedModel: '',
  migration: 0,
  directives: [],
};

export const copilotParams: CopilotParams = {
  async updateApplication(application) {
    await ConnectorSingleton.getInstance().applicationApi.applicationUpdate({
      application,
    });
    const settingValue =
      application.capabilities === CapabilitiesEnum.Blended
        ? 'Blended'
        : 'Local';
    pluginSettings.set('Capabilities', settingValue);
    setStored({
      Capabilities: settingValue,
    });
  },
  runInTerminal(command) {
    const terminal = new TerminalManager();
    terminal.startNew().then(async (session) => {
      await defaultApp.commands.execute('terminal:open', {
        name: session.name,
      });
      session.send({
        type: 'stdin',
        content: [command],
      });
    });
  },
  async getRecentFiles() {
    return { paths: [] };
  },
  async getWorkspacePaths() {
    return { paths: [] };
  },
  migration: 0,
  openFile(path) {
    defaultApp.commands.execute('docmanager:open', {
      path: path,
      options: {
        mode: 'tab-after',
      },
    });
  },
  generateShareableLink: async (
    params: { id: string } | { raw: string; ext: string }
  ) => {
    let link: string | void;
    if ('id' in params) {
      link = await ShareableLinksService.getInstance().generate({
        id: params.id,
      });
      if (link) copyToClipboard(link);
      return { id: params.id };
    } else {
      const asset =
        await ConnectorSingleton.getInstance().assetsApi.assetsCreateNewAsset({
          seed: {
            type: SeedTypeEnum.Asset,
            asset: {
              application: await getApplication(),
              format: {
                fragment: {
                  string: {
                    raw: params.raw,
                  },
                  metadata: {
                    ext: langExtToClassificationSpecificEnum(params.ext),
                  },
                },
              },
            },
          },
        });
      if (asset) {
        link = await ShareableLinksService.getInstance().generate({
          id: asset.id,
        });
        if (link) copyToClipboard(link);
        return { id: asset.id };
      }
    }
  },
  getApplication,
  requestContextPicker: async (
    type: 'files' | 'folders' | 'snippets',
    conversationId: string
  ) => {
    let paths: string[] | null = null;
    if (type === 'files') {
      paths = await ConnectorSingleton.getInstance().osApi.pickFiles({
        filePickerInput: {},
      });
    }
    if (type === 'folders') {
      paths = await ConnectorSingleton.getInstance().osApi.pickFolders();
    }

    if (paths) {
      const anchors = await Promise.all(
        paths.map((path) =>
          ConnectorSingleton.getInstance().anchorsApi.anchorsCreateNewAnchor({
            transferables: false,
            seededAnchor: {
              type:
                type === 'folders'
                  ? AnchorTypeEnum.Directory
                  : AnchorTypeEnum.File,
              fullpath: path,
            },
          })
        )
      );
      QGPTView.lastConversationMessage = new Date();
      for (const anchor of anchors) {
        ConnectorSingleton.getInstance().conversationApi.conversationAssociateAnchor(
          {
            conversation: conversationId,
            anchor: anchor.id,
          }
        );
      }
      return;
    }
    new AddSnippetToContextModal(conversationId).open();
  },
  saveState: (newState: CopilotState) => {
    copilotState = newState;
    PiecesDatabase.writeDB();
  },
  getState: () => {
    return { pieces: copilotState };
  },
  sendNotification: (params: {
    message: string;
    title?: string;
    type: 'info' | 'error' | 'warn';
    actions?: NotificationAction<NotificationActionTypeEnum>[];
  }) => {
    if (params.type === 'info') {
      Notifications.getInstance().information({
        message: params.message,
        actions: params.actions,
      });
    } else {
      Notifications.getInstance().error({
        message: params.message,
        actions: params.actions,
      });
    }
  },
  openLink: (url: string) => window.open(url),
  track: (event: CopilotAnalytics) => {
    SegmentAnalytics.track({ event });
  },
  insertAtCursor(text) {
    //@ts-ignore this does not exist in the api given by jupyterlab, however editor does exist if they have a notebook open.
    const editor = defaultApp.shell.currentWidget?.content.activeCell.editor;
    if (!editor || editor === undefined) {
      Notifications.getInstance().error({
        message: 'Unable to detect editor, cannot insert code.',
      });
      return;
    }
    const selection = document.getSelection();
    editor.replaceSelection(text + selection);
  },
};

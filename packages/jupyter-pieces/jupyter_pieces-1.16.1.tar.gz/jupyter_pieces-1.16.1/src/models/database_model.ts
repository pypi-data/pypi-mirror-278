import { returnedSnippet } from './typedefs';
import { CopilotState } from 'copilot/dist/types/ConversationState';

export default interface PiecesDB {
  assets: returnedSnippet[];
  copilotState: CopilotState;
}

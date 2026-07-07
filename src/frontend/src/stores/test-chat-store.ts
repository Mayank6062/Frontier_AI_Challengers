/**
 * Test file to verify Zustand store behavior
 * This file can be run in Node.js or in browser console
 */

import { useChatStore } from './chat.store';
import { ChatMessage } from '../types';

// Test 1: Verify addMessage updates the store
console.log('Test 1: Verify addMessage updates store');
console.log('Initial messages:', useChatStore.getState().messages);

const testMessage: ChatMessage = {
  id: 'test-1',
  session_id: 'session-123',
  role: 'user',
  content: 'Test message',
  timestamp: new Date().toISOString(),
};

useChatStore.getState().addMessage(testMessage);
console.log('After addMessage:', useChatStore.getState().messages);

// Test 2: Verify reset works
console.log('\nTest 2: Verify resetChat clears messages');
useChatStore.getState().resetChat();
console.log('After reset:', useChatStore.getState().messages);

// Test 3: Verify subscription
console.log('\nTest 3: Verify store subscription');
let subscriptionCalls = 0;
const unsubscribe = useChatStore.subscribe(
  (state) => state.messages,
  (messages) => {
    subscriptionCalls++;
    console.log(`Subscription triggered (call #${subscriptionCalls}):`, messages);
  }
);

console.log('Adding message via subscription...');
useChatStore.getState().addMessage(testMessage);

console.log('Cleanup...');
unsubscribe();

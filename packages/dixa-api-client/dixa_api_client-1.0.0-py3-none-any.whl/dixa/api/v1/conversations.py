from .. import DixaResource, DixaVersion


class ConversationResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/
    """

    resource = "conversations"
    dixa_version: DixaVersion = "v1"

    def add_internal_note(self, conversation_id: str, body):
        """Add an internal note to a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversationsConversationidNotes
        """
        return self.client.post(f"{self.url}/{conversation_id}/notes", body)

    def add_internal_notes(self, conversation_id: str, body):
        """Add internal notes to a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversationsConversationidNotesBulk
        """
        return self.client.post(f"{self.url}/{conversation_id}/notes/bulk", body)

    def add_message(self, conversation_id: str, body):
        """Add a message to a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversationsConversationidMessages
        """
        return self.client.post(f"{self.url}/{conversation_id}/messages", body)

    def anonymize(self, conversation_id: str):
        """Anonymize a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversationsConversationidAnonymize
        """
        return self.client.patch(f"{self.url}/{conversation_id}/anonymize")

    def anonymize_message(self, conversation_id: str, message_id: str):
        """Anonymize message in a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/patchConversationsConversationidMessagesMessageidAnonymize
        """
        return self.client.patch(
            f"{self.url}/{conversation_id}/messages/{message_id}/anonymize"
        )

    def claim(self, conversation_id: str, body):
        """Claim a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/putConversationsConversationidClaim
        """
        return self.client.put(f"{self.url}/{conversation_id}/claim", body)

    def close(self, conversation_id: str, body):
        """Close a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversationsConversationidClose
        """
        return self.client.put(f"{self.url}/{conversation_id}/close", body)

    def create(self, body):
        """Create a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/postConversations
        """
        return self.client.post(self.url, body)

    def get(self, conversation_id: str):
        """Get an conversation by id.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationid
        """
        return self.client.get(f"{self.url}/{conversation_id}")

    def list_activity_logs(self, conversation_id: str):
        """List activity logs.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidActivitylog
        """
        return self.client.get(f"{self.url}/{conversation_id}/activitylog")

    def list_flows(self, conversation_id: str, query: dict | None = None):
        """List flows.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsFlows
        """
        return self.client.get(f"{self.url}/{conversation_id}/flows", query)

    def list_internal_notes(self, conversation_id: str):
        """List internal notes.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidNotes
        """
        return self.client.get(f"{self.url}/{conversation_id}/notes")

    def list_linked_conversations(self, conversation_id: str):
        """List linked conversations.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidLinked
        """
        return self.client.get(f"{self.url}/{conversation_id}/linked")

    def list_messages(self, conversation_id: str):
        """List messages.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidMessages
        """
        return self.client.get(f"{self.url}/{conversation_id}/messages")

    def list_organization_activity_log(self, conversation_id: str):
        """List organization activity log.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsActivitylog
        """
        return self.client.get(f"{self.url}/{conversation_id}/activitylog")

    def list_rating(self, conversation_id: str):
        """List rating.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidRating
        """
        return self.client.get(f"{self.url}/{conversation_id}/rating")

    def list_tags(self, conversation_id: str):
        """List tags.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getConversationsConversationidTags
        """
        return self.client.get(f"{self.url}/{conversation_id}/tags")

    def patch_conversation_custom_attributes(self, conversation_id: str, body):
        """Patch conversation custom attributes.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/patchConversationsConversationidCustom-attributes
        """
        return self.client.patch(
            f"{self.url}/{conversation_id}/custom-attributes", body
        )

    def reopen(self, conversation_id: str, body):
        """Reopen a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/putConversationsConversationidReopen
        """
        return self.client.put(f"{self.url}/{conversation_id}/reopen", body)

    def search(self, query):
        """Search conversations.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/getSearchConversations
        """
        return self.client.get(f"{self.url}/search", query)

    def tag(self, conversation_id: str, tag_id: str):
        """Tag a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/putConversationsConversationidTagsTagid
        """
        return self.client.post(f"{self.url}/{conversation_id}/tags/{tag_id}")

    def untag(self, conversation_id: str, tag_id: str):
        """Untag a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/deleteConversationsConversationidTagsTagid
        """
        return self.client.delete(f"{self.url}/{conversation_id}/tags/{tag_id}")

    def transfer(self, conversation_id: str, body):
        """Transfer a conversation.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Conversations/#tag/Conversations/operation/putConversationsConversationidTransferQueue
        """
        return self.client.post(f"{self.url}/{conversation_id}/transfer/queue", body)

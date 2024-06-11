from mtai.base import MTAIBase


class Prompt(MTAIBase):
    """Prompt Class used across defined."""

    @classmethod
    def list(cls):
        """
        List all prompts.
        Returns:
            JSON Response
        """
        return cls().requests.get("/prompts/list")

    @classmethod
    def ask_question(cls, prompt):
        """
        Create a new response from prompt.
        Args:
            prompt: str
        Returns:
            JSON Response
        """
        return cls().requests.post(
            "/prompts/generate-from-prompt", data={"prompt": prompt}
        )

    @classmethod
    def get_prompt_by_id(cls, promt_id):
        """
        Get a prompt by id.
        Args:
            prompt_id: str
        Returns:
            JSON Response
        """
        return cls().requests.get(f"/prompts/retrieve/{promt_id}")

    @classmethod
    def delete_prompt_by_id(cls, promt_id):
        """
        Delete a prompt by id.
        Args:
            prompt_id: str
        Returns:
            JSON Response
        """
        return cls().requests.delete(f"/prompts/delete/{promt_id}")

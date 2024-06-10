from mtai.base import MTAIBase


class Tag(MTAIBase):
    """Tag Class used across defined."""

    @classmethod
    def list(cls):
        """
        List all tags.
        Returns:
            JSON Response
        """
        return cls().requests.get("/tags/list")

    @classmethod
    def create_from_title(cls, title):
        """
        Create a new tag from title.
        Args:
            title: str
        Returns:
            JSON Response
        """
        return cls().requests.post("/tags/create-from-title", data={"title": title})

    @classmethod
    def create_from_title_summary(cls, title, summary, count=5):
        """
        Create a new tag from title and summary.
        Args:
            title: str
            summary: str
            count: int (default 5)
        Returns:
            JSON Response
        """
        return cls().requests.post(
            "/tags/create-tags-from-title-summary",
            data={"title": title, "summary": summary, "count": count},
        )

    @classmethod
    def get_tag_by_id(cls, tag_id):
        """
        Get a tag by id.
        Args:
            tag_id: str
        Returns:
            JSON Response
        """
        return cls().requests.get(f"/tags/retrieve/{tag_id}")

    @classmethod
    def delete_tag_by_id(cls, tag_id):
        """
        Delete a tag by id.
        Args:
            tag_id: str
        Returns:
            JSON Response
        """
        return cls().requests.delete(f"/tags/delete/{tag_id}")

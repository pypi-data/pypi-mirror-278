from .models import User, ChatSession, SimilarQuestion

def save_to_database(user_name, **kwargs):
    """
    Saves dynamic question-answer pair data to the database.

    Args:
        user_name (str): Username of the question asker.
        **kwargs (dict): Additional keyword arguments containing the session data.

    Returns:
        tuple: A tuple containing the ChatSession and SimilarQuestion objects, or None if an error occurred.
    """
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        print(f"User '{user_name}' not found.")
        return None

    try:
        chat_session = ChatSession.objects.create(user=user, data=kwargs)
        chat_session.save()

        similar_question = SimilarQuestion.objects.create(user=user, data=kwargs)
        similar_question.save()

        return chat_session, similar_question
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

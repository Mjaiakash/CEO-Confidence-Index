from __future__ import annotations


def build_topics(documents: list[str], min_topic_size: int = 5):
    from bertopic import BERTopic
    model = BERTopic(min_topic_size=min_topic_size, verbose=False)
    topics, _ = model.fit_transform(documents)
    return model, model.get_topic_info(), topics

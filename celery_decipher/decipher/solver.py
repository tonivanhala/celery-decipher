from collections import Counter
from random import random, sample, shuffle

from langdetect import PROFILES_DIRECTORY, DetectorFactory
from rapidfuzz.distance import Levenshtein
from rapidfuzz.process import extractOne

from celery_decipher.decipher.cipher import CipherMap, decipher
from celery_decipher.decipher.fixtures import (
    most_common_english_bigrams,
    most_common_english_letters,
    most_common_english_words,
)

_detector_factory = None

MAX_ITERATIONS = 1000


def init_detect() -> DetectorFactory:
    global _detector_factory
    if _detector_factory is None:
        _detector_factory = DetectorFactory()
        _detector_factory.load_profile(PROFILES_DIRECTORY)
    return _detector_factory


def langdetect_fitness(deciphered_text: str) -> float:
    """How well does the deciphered text match English?"""
    if not _detector_factory:
        init_detect()
    detector = _detector_factory.create()
    detector.append(deciphered_text)
    probabilities = detector.get_probabilities()
    try:
        return next(lang.prob for lang in probabilities if lang.lang == "en")
    except StopIteration:
        return 0.0


def word_fitness(deciphered_text: str) -> float:
    """How many words in the deciphered text are close to the English dictionary?"""
    words = {
        "".join(filter(lambda ch: ch.isalpha(), word)).lower()
        for word in deciphered_text.split()
    }
    word_count = len(words)
    if word_count == 0:
        return 0.0
    scores = []
    for word in words:
        best_match = extractOne(
            word, most_common_english_words, scorer=Levenshtein.normalized_similarity
        )
        scores.append(best_match[1])

    return sum(scores) / word_count


def _calculate_probabilities(count_dict: dict[str, int]) -> dict[str, float]:
    total = sum(count_dict.values())
    if total == 0:
        return {k: 0.0 for k in count_dict}
    return {k: v / total for k, v in count_dict.items()}


ENGLISH_BIGRAM_PROBABILITIES = _calculate_probabilities(most_common_english_bigrams)


def _extract_bigrams(text: str) -> dict[str, int]:
    """Extract bigrams from the text."""
    cleaned_text = "".join(filter(lambda ch: ch.isalpha(), text)).lower()

    if len(cleaned_text) < 2:
        return {}

    return Counter[str](cleaned_text[i : i + 2] for i in range(len(cleaned_text) - 1))


def _calculate_bigram_distance(
    text_probabilities: dict[str, float],
    reference_probabilities: dict[str, float],
) -> float:
    total_ssd = 0.0
    num_compared = 0

    for bigram, eng_prob in reference_probabilities.items():
        text_prob = text_probabilities.get(bigram, 0.0)
        total_ssd += (text_prob - eng_prob) ** 2
        num_compared += 1

    return total_ssd / num_compared


def bigram_fitness(deciphered_text: str) -> float:
    deciphered_bigram_counts = _extract_bigrams(deciphered_text)
    deciphered_bigram_probabilities = _calculate_probabilities(deciphered_bigram_counts)

    if not deciphered_bigram_probabilities:
        return 0.0

    distance = _calculate_bigram_distance(
        deciphered_bigram_probabilities, ENGLISH_BIGRAM_PROBABILITIES
    )

    return 1.0 / (1.0 + distance)


def fitness(deciphered_text: str) -> float:
    return (
        word_fitness(deciphered_text)
        * langdetect_fitness(deciphered_text)
        * bigram_fitness(deciphered_text)
    ) ** (1 / 3)


def fill_in_missing_values(cipher_map: CipherMap) -> CipherMap:
    """Fill in missing values in the cipher map."""
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    missing_keys = list(k for k in alphabet if k not in cipher_map)
    missing_values = list(v for v in alphabet if v not in cipher_map.values())
    # create random pairings
    for k, v in zip(missing_keys, missing_values):
        cipher_map[k] = v
    return cipher_map


def crossover(parent1: CipherMap, parent2: CipherMap) -> CipherMap:
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    shuffle(alphabet)
    preference_order: tuple[CipherMap, CipherMap] = (parent1, parent2)
    child_map = {}
    for k in alphabet:
        for i, p in enumerate(preference_order):
            target_value = p.get(k)
            if target_value in child_map.values():
                continue
            child_map[k] = target_value
            # prefer unselected parent next
            preference_order = (preference_order[1 - i], preference_order[i])
            break

    child_map = fill_in_missing_values(child_map)
    return child_map


def mutate(cipher_map: CipherMap, mutation_rate: float = 0.15) -> CipherMap:
    """Mutate the cipher map by swapping two mappings."""
    mutated_map = {k: v for k, v in cipher_map.items()}
    alphabet_keys = [k for k in cipher_map.keys()]
    if random() < mutation_rate:
        k1, k2 = sample(alphabet_keys, 2)
        mutated_map[k1], mutated_map[k2] = mutated_map[k2], mutated_map[k1]
    return mutated_map


def initial_guess_letter_frequencies(cipher_text: str) -> CipherMap:
    # remove punctuation and whitespace
    cipher_text = "".join(filter(lambda ch: ch.isalpha(), cipher_text))
    counter = Counter[str](cipher_text.lower())
    cipher_map = {
        k: v
        for k, (v, _) in zip(
            most_common_english_letters,
            sorted(counter.items(), key=lambda item: item[1], reverse=True),
        )
    }
    cipher_map = fill_in_missing_values(cipher_map)
    return cipher_map


def get_random_cipher_map() -> CipherMap:
    """Generate a random cipher map."""
    sources = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    targets = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    cipher_map = {}
    shuffle(sources)
    for k in sources:
        cipher_map[k] = targets.pop()
    return cipher_map


def _run_tournament(
    cipher_text: str, candidates: list[CipherMap], tournament_size: int
) -> CipherMap:
    """Run a tournament to select the best candidate."""
    tournament = sample(candidates, tournament_size)
    best_candidate = max(
        tournament, key=lambda item: fitness(decipher(cipher_text, item))
    )
    return best_candidate


def run_full_solver(cipher_text: str) -> CipherMap:
    """Solve the cipher using a genetic algorithm in a single function."""

    population_size = 1000
    elite_size = 20  # Keep top 20 unmodified
    num_random = 50  # Add 5% random
    tournament_size = 3

    cipher_map = initial_guess_letter_frequencies(cipher_text)
    candidates = [get_random_cipher_map() for _ in range(population_size - 10)]
    candidates.extend(mutate(cipher_map, 1.0) for _ in range(10))

    for iteration in range(MAX_ITERATIONS):
        candidates = sorted(
            candidates,
            key=lambda item: fitness(decipher(cipher_text, item)),
            reverse=True,
        )
        deciphered = decipher(cipher_text, candidates[0])
        score = fitness(deciphered)
        print(
            f"{iteration + 1} / {MAX_ITERATIONS} Best fitness: {score}. Candidates: {len(candidates)}. Deciphered: {deciphered}"
        )
        if score > 0.975:
            return candidates[0]

        new_candidates = []

        elite_candidates = candidates[:elite_size]
        new_candidates.extend(elite_candidates)

        num_offspring = population_size - len(new_candidates) - num_random

        for _ in range(num_offspring):
            parent1 = _run_tournament(cipher_text, candidates, tournament_size)
            parent2 = _run_tournament(cipher_text, candidates, tournament_size)

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_candidates.append(child)

        new_candidates.extend(get_random_cipher_map() for _ in range(num_random))

        candidates = new_candidates
    candidates = sorted(
        candidates, key=lambda item: fitness(decipher(cipher_text, item)), reverse=True
    )
    return candidates[0]

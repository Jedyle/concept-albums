from ..parse_lyrics import GeniusClient


def test_get_song_lyrics():
    client = GeniusClient()
    lyrics = client.get_song_lyrics("Mystery", "If You See Her")
    assert (
        lyrics
        == "She stood there\n\n\nSitting all alone under the stairs\n\n\nLaughter echoes from the corridors\n\n\n\n\nYoung people walking all around\n\n\nEverywhere\n\n\nIf only one could've seen a little more\n\n\n\n\nIf you see her\n\n\nTell her about the love she ought to find\n\n\n\n\nNow she's wandering on her own\n\n\nAnywhere\n\n\nTrying to find her way out of this maze\n\n\n\n\nThe scars that cut her to the bones\n\n\nWill remain\n\n\nDespite the smile shining from her eyes\n\n\n\n\nIf you see her\n\n\nTell her about the love she ought to find\n\n\nAnd show her\n\n\nThe beauty of the world she leaves behind\n\n\nShe leaves behind\n\n\nIf you see her\n\n\nTell her about the love she ought to find\n\n\n\n\nThey stand there\n\n\nSitting all around on the stairs\n\n\nHer tears will sing above their silence everywhere\n\n\nThe song she sang to mend all of your hearts\n\n\n\n\nIf you see her\n\n\nTell her about the love she ought to find\n\n\nAnd show her\n\n\nThe beauty of the world she leaves behind\n\n\nShe leaves behind"
    )

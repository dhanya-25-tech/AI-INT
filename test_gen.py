import time
import urllib.parse
import requests
import concurrent.futures

prompts = [
    'Scandinavian minimalist bathroom design with glass shower',
    'Modern Japanese zen minimalist bathroom with teak bathtub',
    'Sleek luxury marble minimalist bathroom with floating vanity',
    'Minimalist white tile bathroom with matte black fixtures',
    'Organic minimalist bathroom with travertine stone walls'
]

def gen(i, p):
    t0 = time.time()
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=768&height=768&seed={1000+i*77}&nologo=true"
    res = requests.get(url, timeout=15)
    return i, res.status_code, len(res.content), round(time.time() - t0, 2)

if __name__ == "__main__":
    t_start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        futures = [ex.submit(gen, i, p) for i, p in enumerate(prompts)]
        results = [f.result() for f in futures]
    print(f"Total parallel execution time: {time.time() - t_start:.2f}s")
    for r in results:
        print(f"Variation #{r[0]+1}: HTTP {r[1]}, Bytes {r[2]}, Elapsed {r[3]}s")

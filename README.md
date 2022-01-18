# Start
Note! Python3.x required
```py
pip install -r req.txt
python main.py
```

# How it works
1. Script read the all list of company ids
2. Then it start to scrape companies about, one by one
3. After it start to scrape companies reviews, one by one
4. Then it link companies and reviews together and save to `result.json`

Failed requests have `max_retries=3` (if request failed or Selenium can not scrape the data)

# Shortly about
* Since GlassDoor uses Cloudflare for ant-fraud protection, I had to use `undetected_chromedriver`
* When I started this task, I decided to use default selenium parsing solutions. But I didn't like the performance at all, it took more than 1 minute to scrape one page
* So I started inspecting the JavaScript of GlassDoor
* And I found that they use something like `State-Manager` called Apollo-State
* The best way is to implement the parser of GlassDoor javascript state
* That was exactly the silver bullet! This improved performance by over 95%

So the tip is to inspect/reverse a JavaScript sources of the web-site firstly!

# How to improve
To scale the scraper we can use something like `Kubernetes` to scale up the instances of scraper. Other than that we should use `MQ` services (s.e `RabbitMQ`, `Kafka`) to transfer urls to the scrapers. So an example architecture should look like this:

![There should be a picture here](https://gist.github.com/pryvated/be47ec1713348d1b68bcdfa16ad21693/raw/55140e25471fe912fc393a07b704009d0fc694da/figma_frame.png)
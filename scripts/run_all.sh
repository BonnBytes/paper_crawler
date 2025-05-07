pip install .

# crawl paper links
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo crawling papers from: $icmlconf
    python -m paper_crawler.crawl_links_soup --id "$icmlconf"
done

#python -m paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo crawling papers from: $nipsconf
    python -m paper_crawler.crawl_links_soup --id "$nipsconf"
done

#python -m paper_crawler.crawl_links_openreview --id ICLR.cc/2024/Conference
for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo crawling papers from: $iclrconf
    python -m paper_crawler.crawl_links_openreview --id "$iclrconf"
done


# filter links and download soup
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo looking at links for: $icmlconf
    python -m paper_crawler.filter_and_download_links --id "$icmlconf"
done

#python -m paper_crawler.filter_and_download_links --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo looking at links for: $nipsconf
    python -m paper_crawler.filter_and_download_links --id "$nipsconf"
done

for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo looking at links for: $iclrconf
    python -m paper_crawler.filter_and_download_links --id "$iclrconf"
done

# process pages
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo processing pages for: $icmlconf
    python -m paper_crawler.process_pages --id "$icmlconf"
done

#python -m paper_crawler.process_pages --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo processing pages for: $nipsconf
    python -m paper_crawler.process_pages --id "$nipsconf"
done

for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo processing pages for: $iclrconf
    python -m paper_crawler.process_pages --id "$iclrconf"
done

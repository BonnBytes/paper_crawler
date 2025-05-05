# crawl paper links
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    python -m paper_crawler.crawl_links_soup --id "$icmlconf"
done

#python -m paper_crawler.crawl_links_openreview --id ICLR.cc/2024/Conference
for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    python -m paper_crawler.crawl_links_openreview --id "$iclrconf"
done

#python -m paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for nipsconf in NeurIPS.cc/2024/Conference NeurIPS.cc/2023/Conference NeurIPS.cc/2022/Conference NeurIPS.cc/2021/Conference NeurIPS.cc/2020/Conference NeurIPS.cc/2019/Conference NeurIPS.cc/2018/Conference NeurIPS.cc/2017/Conference NeurIPS.cc/2016/Conference NeurIPS.cc/2015/Conference NeurIPS.cc/2014/Conference; do
    python -m paper_crawler.crawl_links_openreview --id "$nipsconf"
done

# filter links and download soup
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    python -m paper_crawler.filter_and_download_links --id "$icmlconf"
done

for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    python -m paper_crawler.filter_and_download_links --id "$iclrconf"
done

#python -m paper_crawler.filter_and_download_links --id NeurIPS.cc/2024/Conference
for nipsconf in NeurIPS.cc/2024/Conference NeurIPS.cc/2023/Conference NeurIPS.cc/2022/Conference NeurIPS.cc/2021/Conference NeurIPS.cc/2020/Conference NeurIPS.cc/2019/Conference NeurIPS.cc/2018/Conference NeurIPS.cc/2017/Conference NeurIPS.cc/2016/Conference NeurIPS.cc/2015/Conference NeurIPS.cc/2014/Conference; do
    python -m paper_crawler.filter_and_download_links --id "$nipsconf"
done

# process pages
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    python -m paper_crawler.process_pages --id "$icmlconf"
done

for iclrconf in ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    python -m paper_crawler.process_pages --id "$iclrconf"
done

#python -m paper_crawler.process_pages --id NeurIPS.cc/2024/Conference
for nipsconf in NeurIPS.cc/2024/Conference NeurIPS.cc/2023/Conference NeurIPS.cc/2022/Conference NeurIPS.cc/2021/Conference NeurIPS.cc/2020/Conference NeurIPS.cc/2019/Conference NeurIPS.cc/2018/Conference NeurIPS.cc/2017/Conference NeurIPS.cc/2016/Conference NeurIPS.cc/2015/Conference NeurIPS.cc/2014/Conference; do
    python -m paper_crawler.process_pages --id "$nipsconf"
done

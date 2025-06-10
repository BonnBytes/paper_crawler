pip install .

echo crawling papers from tmlr
python -m paper_crawler.crawl_tmlr

for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo crawling papers from: $iclrconf
    python -m src.paper_crawler.crawl_links_openreview --id "$iclrconf"
done

# crawl paper links
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo crawling papers from: $icmlconf
    python -m paper_crawler.crawl_links_soup --id "$icmlconf"
done

# python -m paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for aistatsconf in aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017 aistats2016 aistats2015 aistats2014; do
    echo crawling papers from: $aistatsconf
    python -m paper_crawler.crawl_links_soup --id "$aistatsconf"
done

# python -m paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo crawling papers from: $nipsconf
    python -m paper_crawler.crawl_links_soup --id "$nipsconf"
done

echo looking at links for TMLR
python -m paper_crawler.filter_and_download_links --id tmlr


echo looking at links for ICLR
for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo crawling papers from $iclrconf
    python -m paper_crawler.filter_and_download_links --id "$iclrconf"
done

# filter links and download soup
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo looking at links for: $icmlconf
    python -m paper_crawler.filter_and_download_links --id "$icmlconf"
done

for aistatsconf in aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017 aistats2016 aistats2015 aistats2014; do
    echo looking at links for: $aistatsconf
    python -m paper_crawler.filter_and_download_links --id "$aistatsconf"
done

# python -m paper_crawler.filter_and_download_links --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo looking at links for: $nipsconf
    python -m paper_crawler.filter_and_download_links --id "$nipsconf"
done

echo processing pages for tmlr
python -m paper_crawler.process_pages --id tmlr

echo processing pages for ICLR
for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2019/Conference ICLR.cc/2018/Conference ICLR.cc/2017/Conference ICLR.cc/2016/Conference ICLR.cc/2015/Conference ICLR.cc/2014/Conference; do
    echo crawling papers from $iclrconf
    python -m src.paper_crawler.process_pages --id "$iclrconf"
done

# process pages
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo processing pages for: $icmlconf
    python -m paper_crawler.process_pages --id "$icmlconf"
done

for aistatsconf in aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017 aistats2016 aistats2015 aistats2014; do
    echo processing pages for: $aistatsconf
    python -m paper_crawler.process_pages --id "$aistatsconf"
done

# python -m paper_crawler.process_pages --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo processing pages for: $nipsconf
    python -m paper_crawler.process_pages --id "$nipsconf"
done


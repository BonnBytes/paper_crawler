pip install .

echo crawling papers from jmlr
python -m src.paper_crawler.crawl_jmlr

for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2017/conference; do
    echo crawling papers from: $iclrconf
    python -m src.paper_crawler.crawl_links_openreview --id "$iclrconf"
done

# crawl paper links from iclrs where openreview did not work.
for iclrconf in iclr2019 iclr2018 iclr2016; do
    echo crawling papers from: $iclrconf
    python -m src.paper_crawler.crawl_links_soup --id "$iclrconf"
done

# crawl paper links
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo crawling papers from: $icmlconf
    python -m src.paper_crawler.crawl_links_soup --id "$icmlconf"
done

# python -m src.paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for aistatsconf in aistats2025 aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017; do
    echo crawling papers from: $aistatsconf
    python -m src.paper_crawler.crawl_links_soup --id "$aistatsconf"
done

# python -m src.paper_crawler.crawl_links_openreview --id NeurIPS.cc/2024/Conference
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo crawling papers from: $nipsconf
    python -m src.paper_crawler.crawl_links_soup --id "$nipsconf"
done

echo looking at links for TMLR
python -m src.paper_crawler.filter_and_download_links --id tmlr
echo looking at links for mloss
python -m src.paper_crawler.filter_and_download_links --id mloss


echo looking at links for ICLR
for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2017/conference; do
    echo crawling papers from $iclrconf
    python -m src.paper_crawler.filter_and_download_links --id "$iclrconf"
done

# iclrs where openreview did not work.
for iclrconf in iclr2019 iclr2018 iclr2016; do
    echo crawling papers from: $iclrconf
    python -m src.paper_crawler.filter_and_download_links --id "$iclrconf"
done


# filter links and download soup
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo looking at links for: $icmlconf
    python -m src.paper_crawler.filter_and_download_links --id "$icmlconf"
done

for aistatsconf in aistats2025 aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017; do
    echo looking at links for: $aistatsconf
    python -m src.paper_crawler.filter_and_download_links --id "$aistatsconf"
done

# python -m src.paper_crawler.filter_and_download_links --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo looking at links for: $nipsconf
    python -m src.paper_crawler.filter_and_download_links --id "$nipsconf"
done

echo processing pages for tmlr
python -m src.paper_crawler.process_pages --id tmlr
python -m src.paper_crawler.process_pages --id mloss

echo processing pages for ICLR
for iclrconf in ICLR.cc/2025/Conference ICLR.cc/2024/Conference ICLR.cc/2023/Conference ICLR.cc/2022/Conference ICLR.cc/2021/Conference ICLR.cc/2020/Conference ICLR.cc/2017/conference; do
    echo process_pages from $iclrconf
    python -m src.src.paper_crawler.process_pages --id "$iclrconf"
done

for iclrconf in iclr2019 iclr2018 iclr2016; do
    echo crawling papers from: $iclrconf
    python -m src.paper_crawler.process_pages --id "$iclrconf"
done

# process pages
for icmlconf in icml2024 icml2023 icml2022 icml2021 icml2020 icml2019 icml2018 icml2017 icml2016 icml2015 icml2014; do
    echo processing pages for: $icmlconf
    python -m src.paper_crawler.process_pages --id "$icmlconf"
done

for aistatsconf in aistats2025 aistats2024 aistats2023 aistats2022 aistats2021 aistats2020 aistats2019 aistats2018 aistats2017; do
    echo processing pages for: $aistatsconf
    python -m src.paper_crawler.process_pages --id "$aistatsconf"
done

# python -m src.paper_crawler.process_pages --id nips2024
for nipsconf in nips2024 nips2023 nips2022 nips2021 nips2020 nips2019 nips2018 nips2017 nips2016 nips2015 nips2014; do
    echo processing pages for: $nipsconf
    python -m src.paper_crawler.process_pages --id "$nipsconf"
done


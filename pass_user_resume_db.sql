select
   pass_r_no
  ,replace(replace(m_id                  ,char(13),\'\'),char(10),\'\') as m_id 
  ,replace(replace(m_name                ,char(13),\'\'),char(10),\'\') as m_name 
  ,replace(replace(m_email               ,char(13),\'\'),char(10),\'\') as m_email 
  ,replace(replace(m_homepage            ,char(13),\'\'),char(10),\'\') as m_homepage 
  ,replace(replace(m_addr_text           ,char(13),\'\'),char(10),\'\') as m_addr_text 
  ,replace(replace(m_home_phone          ,char(13),\'\'),char(10),\'\') as m_home_phone 
  ,replace(replace(m_hand_phone          ,char(13),\'\'),char(10),\'\') as m_hand_phone 
  ,pass_resume_type
  ,pass_no
  ,replace(replace(m_live_resume         ,char(13),\'\'),char(10),\'\') as m_live_resume 
  ,m_gender  
  ,replace(replace(gg_part_no            ,char(13),\'\'),char(10),\'\') as gg_part_no 
  ,replace(replace(gg_want_area_no       ,char(13),\'\'),char(10),\'\') as gg_want_area_no 
  ,m_last_edu_level
  ,m_career_level
  ,m_career_month
  ,replace(replace(m_job_type            ,char(13),\'\'),char(10),\'\') as m_job_type 
  ,m_want_pay
  ,replace(replace(m_career_text         ,char(13),\'\'),char(10),\'\') as m_career_text 
  ,replace(replace(m_licence_text        ,char(13),\'\'),char(10),\'\') as m_licence_text 
  ,m_language_stat  
  ,replace(replace(m_lang_search         ,char(13),\'\'),char(10),\'\') as m_lang_search 
  ,replace(replace(m_lang_con            ,char(13),\'\'),char(10),\'\') as m_lang_con 
  ,replace(replace(m_lan_etc_text        ,char(13),\'\'),char(10),\'\') as m_lan_etc_text 
  ,replace(replace(m_oa_stat             ,char(13),\'\'),char(10),\'\') as m_oa_stat 
  ,replace(replace(m_skill_text          ,char(13),\'\'),char(10),\'\') as m_skill_text 
  ,replace(replace(m_keyword             ,char(13),\'\'),char(10),\'\') as m_keyword 
  ,replace(replace(m_resume_title        ,char(13),\'\'),char(10),\'\') as m_resume_title 
  ,replace(replace(m_profile_text        ,char(13),\'\'),char(10),\'\') as m_profile_text 
  ,replace(replace(m_pdf_resume          ,char(13),\'\'),char(10),\'\') as m_pdf_resume 
  ,pass_resume_w_date  
  ,m_e_date  
  ,gg_oem_no  
  ,replace(replace(m_detail_stat         ,char(13),\'\'),char(10),\'\') as m_detail_stat 
  ,replace(replace(m_edu_text            ,char(13),\'\'),char(10),\'\') as m_edu_text 
  ,m_disabled_stat  
  ,m_portfolio_stat  
  ,replace(replace(attach_file_name      ,char(13),\'\'),char(10),\'\') as attach_file_name 
  ,replace(replace(attach_file_title     ,char(13),\'\'),char(10),\'\') as attach_file_title 
  ,r_input_stat
  ,template
  ,m_image_stat  
  ,m_file_stat  
  ,replace(replace(career_oidx           ,char(13),\'\'),char(10),\'\') as career_oidx 
  ,replace(replace(career_ccode          ,char(13),\'\'),char(10),\'\') as career_ccode 
  ,replace(replace(areacode              ,char(13),\'\'),char(10),\'\') as areacode 
  ,replace(replace(m_edu_con             ,char(13),\'\'),char(10),\'\') as m_edu_con 
  ,replace(replace(m_born                ,char(13),\'\'),char(10),\'\') as m_born 
  ,replace(replace(m_photo_name          ,char(13),\'\'),char(10),\'\') as m_photo_name 
  ,replace(replace(m_language_point_stat ,char(13),\'\'),char(10),\'\') as m_language_point_stat  
  ,replace(replace(m_handicap_stat       ,char(13),\'\'),char(10),\'\') as m_handicap_stat 
  ,replace(replace(handicap_lev          ,char(13),\'\'),char(10),\'\') as handicap_lev 
  ,m_military_stat
  ,replace(replace(military_sym          ,char(13),\'\'),char(10),\'\') as military_sym 
  ,replace(replace(military_eym          ,char(13),\'\'),char(10),\'\') as military_eym 
  ,military_kind
  ,military_level
  ,replace(replace(m_veteran_stat        ,char(13),\'\'),char(10),\'\') as m_veteran_stat 
  ,r_foreign_stat
  ,r_alba_stat
  ,m_abroad_career_term  
  ,replace(replace(m_abroad_career_area  ,char(13),\'\'),char(10),\'\') as m_abroad_career_area 
  ,m_abroad_career_cnt  
  ,replace(replace(m_license_code        ,char(13),\'\'),char(10),\'\') as m_license_code 
  ,replace(replace(m_license             ,char(13),\'\'),char(10),\'\') as m_license 
  ,m_license_cnt
  ,m_training_cnt  
  ,replace(replace(m_training_code       ,char(13),\'\'),char(10),\'\') as m_training_code 
  ,replace(replace(m_oa_stat_edit        ,char(13),\'\'),char(10),\'\') as m_oa_stat_edit 
  ,job_protect_stat
  ,replace(replace(tndc_type_code        ,char(13),\'\'),char(10),\'\') as tndc_type_code 
  ,replace(replace(chc_item_code         ,char(13),\'\'),char(10),\'\') as chc_item_code 
  ,career_stat
  ,m_career_text_stat
  ,replace(replace(c_name_con            ,char(13),\'\'),char(10),\'\') as c_name_con 
  ,school_perfect  
  ,school_point  
  ,replace(replace(m_school_con          ,char(13),\'\'),char(10),\'\') as m_school_con 
  ,replace(replace(major                 ,char(13),\'\'),char(10),\'\') as major 
  ,replace(replace(grad_degree           ,char(13),\'\'),char(10),\'\') as grad_degree 
  ,replace(replace(pass_lable            ,char(13),\'\'),char(10),\'\') as pass_lable 
  ,replace(replace(will_cntnt            ,char(13),\'\'),char(10),\'\') as will_cntnt 
  ,employ_spprt_trgt_stat
  ,m_want_pay_amt
  ,replace(replace(abn_bizjobtype_code   ,char(13),\'\'),char(10),\'\') as abn_bizjobtype_code
from pass_user_resume_db where pass_r_no = 51206247

